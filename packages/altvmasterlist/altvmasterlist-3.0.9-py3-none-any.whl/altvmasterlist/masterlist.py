#!/usr/bin/env python3
from requests.adapters import HTTPAdapter, Retry
from dataclasses import dataclass
from io import StringIO
from re import compile
from enum import Enum
import requests
import secrets
import logging
import sys

logging.basicConfig(level=logging.INFO)
logging.getLogger().setLevel(logging.INFO)
"""You can find the masterlist api docs here: https://docs.altv.mp/articles/master_list_api.html"""


class MasterlistUrls(Enum):
    """This class is used for the masterlist submodule. It provides all urls needed."""
    all_server_stats = "https://api.alt-mp.com/servers/info"
    all_servers = "https://api.alt-mp.com/servers"
    specific_server = "https://api.alt-mp.com/servers/{}"
    specific_server_average = "https://api.alt-mp.com/servers/{}/avg/{}"
    specific_server_maximum = "https://api.alt-mp.com/servers/{}/max/{}"


class Extra(Enum):
    """This class defines extra values."""
    user_agent = "AltPublicAgent"
    default_password = "17241709254077376921"


@dataclass
class RequestHeaders:
    """These are the common request headers used by the request function.
    They are commonly used to emulate an alt:V client.
    """
    host: str = ""
    user_agent: str = Extra.user_agent.value
    accept: str = '*/*'
    alt_debug: str = 'false'
    alt_password: str = Extra.default_password.value
    alt_branch: str = ""
    alt_version: str = ""
    alt_player_name: str = secrets.token_urlsafe(10)
    alt_social_id: int = "0"
    alt_hardware_id2: str = secrets.token_hex(19)
    alt_hardware_id: str = secrets.token_hex(19)

    def __init__(self, server):
        self.alt_branch = server.branch
        self.alt_version = server.version
        self.host = server.address

    def to_dict(self):
        return {
            'Host': self.host,
            'Alt-Branch': self.alt_branch,
            "Alt-Debug": self.alt_debug,
            'Alt-Hardware-ID': self.alt_hardware_id,
            'Alt-Hardware-ID2': self.alt_hardware_id2,
            'Alt-Password': self.alt_password,
            'Alt-Player-Name': self.alt_player_name,
            'Alt-Social-ID': self.alt_social_id,
            'Alt-Version': self.alt_version,
            'User-Agent': self.user_agent,
            'Accept': self.accept,
            'Origin': f'http://{self.host}',
            'Connection': 'close'
        }


def request(url: str, server: any = None) -> dict | None:
    """This is the common request function to fetch remote data.

    Args:
        url (str): The Url to fetch.
        server (Server): An alt:V masterlist or altstats Server object.

    Returns:
        None: When an error occurred. But exceptions will still be logged!
        json: As data
    """
    # Use the User-Agent: AltPublicAgent, because some servers protect their CDN with
    # a simple User-Agent check e.g. https://luckyv.de does that
    with requests.session() as session:
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        session.mount('http', HTTPAdapter(max_retries=retries))

        if server and "http://" in url and not server.useCdn:
            session.headers = RequestHeaders(server).to_dict()
        else:
            session.headers = {
                'User-Agent': Extra.user_agent.value,
                'content-type': 'application/json; charset=utf-8'
            }

        try:
            api_request = session.get(url, timeout=5)
            if api_request.status_code != 200:
                logging.warning(f"the request returned nothing.")
                return None
            else:
                return api_request.json()
        except Exception as e:
            logging.error(e)
            return None


class Permissions:
    """This is the Permission class used by get_permissions.

    Returns:
        Required: The required permissions of an alt:V server. Without them, you can not play on the server.
        Optional: The optional permissions of an alt:V server. You can play without them.
    """

    @dataclass
    class Required:
        """Required Permissions of an alt:V server.

        Attributes:
        ----------
            screen_capture (bool): This allows a screenshot to be taken of the alt:V process (just GTA) and any webview
            webrtc (bool): This allows peer-to-peer RTC inside JS
            clipboard_access (bool): This allows to copy content to users clipboard
        """
        screen_capture: bool = False
        webrtc: bool = False
        clipboard_access: bool = False

    @dataclass
    class Optional:
        """Optional Permissions of an alt:V server.

        Attributes:
        ----------
            screen_capture (bool): This allows a screenshot to be taken of the alt:V process (just GTA) and any webview
            webrtc (bool): This allows peer-to-peer RTC inside JS
            clipboard_access (bool): This allows to copy content to users clipboard
        """
        screen_capture: bool = False
        webrtc: bool = False
        clipboard_access: bool = False


@dataclass
class Server:
    publicId: str
    """The server id."""
    no_fetch: bool = False
    """Define if you want to fetch the api data. This can be used when we already have data."""
    playersCount: int = 0
    """Current player count"""
    maxPlayersCount: int = 0
    """player limit"""
    passworded: bool = False
    """password protected"""
    language: str = "en"
    """two letter country code"""
    useEarlyAuth: bool = False
    """server is using early auth (https://docs.altv.mp/articles/earlyauth.html)"""
    earlyAuthUrl: str = ""
    """early auth url (usually a login screen)"""
    useCdn: bool = False
    """server is using a cdn (https://docs.altv.mp/articles/cdn.html)"""
    cdnUrl: str = ""
    """cdn url"""
    useVoiceChat: bool = False
    """server is using the built in voice chat (https://docs.altv.mp/articles/voice.html) 
    (https://docs.altv.mp/articles/external_voice_server.html)"""
    version: str = ""
    """server version"""
    branch: str = ""
    """server branch (release, rc, dev)"""
    available: bool = False
    """server is online"""
    banned: bool = False
    name: str = ""
    """server name"""
    vanityUrl: str = ""
    website: str = ""
    """server website"""
    gameMode: str = ""
    """gamemode provided by the server"""
    description: str = ""
    """description provided by the server"""
    tags: str = ""
    """tags provided by the server"""
    lastTimeUpdate: str = ""
    """time string with this format 2024-02-12T16:22:24.195392493Z"""
    verified: bool = False
    """alt:V verified server"""
    promoted: bool = False
    """promoted server"""
    visible: bool = False
    """visible in server-list"""
    hasCustomSkin: bool = False
    bannerUrl: str = ""
    address: str = ""
    """connection address for the client can be url + port or ip + port"""
    """"""
    group: {
        id: str,
        name: str
    } = None

    def __init__(self, server_id: str, no_fetch: bool = False) -> None:
        """Update the server data using the api."""
        self.publicId = server_id

        if not no_fetch:
            temp_data = request(MasterlistUrls.specific_server.value.format(self.publicId))
            if temp_data is None or temp_data == {}:
                # the api returned no data or the server is offline
                self.playersCount = 0
            else:
                self.playersCount = temp_data["playersCount"]
                self.maxPlayersCount = temp_data["maxPlayersCount"]
                self.passworded = temp_data["passworded"]
                self.port = temp_data["port"]
                self.language = temp_data["language"]
                self.useEarlyAuth = temp_data["useEarlyAuth"]
                self.earlyAuthUrl = temp_data["earlyAuthUrl"]
                self.useCdn = temp_data["useCdn"]
                self.cdnUrl = temp_data["cdnUrl"]
                self.useVoiceChat = temp_data["useVoiceChat"]
                self.version = temp_data["version"]
                self.branch = temp_data["branch"]
                self.available = temp_data["available"]
                self.banned = temp_data["banned"]
                self.name = temp_data["name"]
                self.publicId = temp_data["publicId"]
                self.vanityUrl = temp_data["vanityUrl"]
                self.website = temp_data["website"]
                self.gameMode = temp_data["gameMode"]
                self.description = temp_data["description"]
                self.tags = temp_data["tags"]
                self.lastTimeUpdate = temp_data["lastTimeUpdate"]
                self.verified = temp_data["verified"]
                self.promoted = temp_data["promoted"]
                self.visible = temp_data["visible"]
                self.hasCustomSkin = temp_data["hasCustomSkin"]
                self.bannerUrl = temp_data["bannerUrl"]
                self.address = temp_data["address"]
                self.group = temp_data["group"]

    def update(self) -> None:
        """Update the server data using the api."""
        self.__init__(self.publicId)

    def get_max(self, time: str = "1d") -> dict | None:
        """Maximum - Returns maximum data about the specified server (TIME = 1d, 7d, 31d)

        Args:
            time (str): The timerange of the data. Can be 1d, 7d, 31d.

        Returns:
            None: When an error occurs
            dict: The maximum player data
        """
        return request(MasterlistUrls.specific_server_maximum.value.format(self.publicId, time))

    def get_avg(self, time: str = "1d", return_result: bool = False) -> dict | int | None:
        """Averages - Returns averages data about the specified server (TIME = 1d, 7d, 31d)

        Args:
            time (str): The timerange of the data. Can be 1d, 7d, 31d.
            return_result (bool): Define if you want the overall average.

        Returns:
            None: When an error occurs
            dict: The maximum player data
            int: Overall average of defined timerange
        """
        average_data = request(MasterlistUrls.specific_server_average.value.format(self.publicId, time))
        if not average_data:
            return None

        if return_result:
            players_all = 0
            for entry in average_data:
                players_all = players_all + entry["c"]
            result = players_all / len(average_data)
            return round(result)
        else:
            return average_data

    @property
    def connect_json(self) -> dict | None:
        """This function fetched the connect.json of an alt:V server.

        Returns:
            None: When an error occurred. But exceptions will still be logged!
            dict: The connect.json
        """
        if not self.available or self.passworded:
            return None

        if not self.useCdn:
            # This Server is not using a CDN.
            cdn_request = request(f"http://{self.address}/connect.json", self)
            if cdn_request is None:
                # possible server error or blocked
                return None
            else:
                return cdn_request
        else:
            # let`s try to get the connect.json
            match self.cdnUrl:
                case _ if ":80" in self.cdnUrl:
                    cdn_request = request(f"http://{self.cdnUrl.replace(':80', '')}/connect.json", self)
                case _ if ":443" in self.cdnUrl:
                    cdn_request = request(f"https://{self.cdnUrl.replace(':443', '')}/connect.json", self)
                case _:
                    cdn_request = request(f"{self.cdnUrl}/connect.json", self)

            if cdn_request is None:
                # maybe the CDN is offline
                return None
            else:
                return cdn_request

    @property
    def permissions(self) -> Permissions | None:
        """This function returns the Permissions defined by the server. https://docs.altv.mp/articles/permissions.html

        Returns:
            None: When an error occurred. But exceptions will still be logged!
            Permissions: The permissions of the server.
        """

        class Permission(Enum):
            screen_capture = "Screen Capture"
            webrtc = "WebRTC"
            clipboard_access = "Clipboard Access"
            optional = "optional-permissions"
            required = "required-permissions"

        connect_json = self.connect_json

        optional = connect_json[Permission.optional.value]
        required = connect_json[Permission.required.value]

        permissions = Permissions()

        if optional is not []:
            try:
                permissions.Optional.screen_capture = optional[Permission.screen_capture.value]
            except TypeError:
                pass

            try:
                permissions.Optional.webrtc = optional[Permission.webrtc.value]
            except TypeError:
                pass

            try:
                permissions.Optional.clipboard_access = optional[Permission.clipboard_access.value]
            except TypeError:
                pass

        if required is not []:
            try:
                permissions.Required.screen_capture = required[Permission.screen_capture.value]
            except TypeError:
                pass

            try:
                permissions.Required.webrtc = required[Permission.webrtc.value]
            except TypeError:
                pass

            try:
                permissions.Required.clipboard_access = required[Permission.clipboard_access.value]
            except TypeError:
                pass

        return permissions

    def get_dtc_url(self, password=None) -> str | None:
        """This function gets the direct connect protocol url of an alt:V Server.
        (https://docs.altv.mp/articles/connectprotocol.html)

        Args:
            password (str): The password of the server.

        Returns:
            None: When an error occurred. But exceptions will still be logged!
            str: The direct connect protocol url.
        """
        with StringIO() as dtc_url:
            if self.useCdn:
                if "http" not in self.cdnUrl:
                    dtc_url.write(f"altv://connect/http://{self.cdnUrl}")
                else:
                    dtc_url.write(f"altv://connect/{self.cdnUrl}")
            else:
                dtc_url.write(f"altv://connect/{self.address}")

            if self.passworded and password is None:
                logging.warning(
                    "Your server is password protected but you did not supply a password for the Direct Connect Url.")

            if password is not None:
                dtc_url.write(f"?password={password}")

            return dtc_url.getvalue()


def get_server_stats() -> dict | None:
    """Statistics - Player Count across all servers & The amount of servers online

    Returns:
        None: When an error occurs
        dict: The stats
    """
    data = request(MasterlistUrls.all_server_stats.value)
    if data is None:
        return None
    else:
        return data


def get_servers() -> list[Server] | None:
    """Generates a list of all servers that are currently online.
    Note that the server objects returned are not complete!

    Returns:
        None: When an error occurs
        list: List object that contains all servers.
    """
    return_servers = []
    servers = request(MasterlistUrls.all_servers.value)
    if servers is None or servers == "{}":
        return None
    else:
        for server in servers:
            tmp_server = Server(server["publicId"], no_fetch=True)
            tmp_server.playersCount = server["playersCount"]
            tmp_server.maxPlayersCount = server["maxPlayersCount"]
            tmp_server.passworded = server["passworded"]
            tmp_server.language = server["language"]
            tmp_server.useEarlyAuth = server["useEarlyAuth"]
            tmp_server.earlyAuthUrl = server["earlyAuthUrl"]
            tmp_server.useCdn = server["useCdn"]
            tmp_server.cdnUrl = server["cdnUrl"]
            tmp_server.useVoiceChat = server["useVoiceChat"]
            tmp_server.version = server["version"]
            tmp_server.branch = server["branch"]
            tmp_server.available = server["available"]
            tmp_server.banned = server["banned"]
            tmp_server.name = server["name"]
            tmp_server.publicId = server["publicId"]
            tmp_server.vanityUrl = server["vanityUrl"]
            tmp_server.website = server["website"]
            tmp_server.gameMode = server["gameMode"]
            tmp_server.description = server["description"]
            tmp_server.tags = server["tags"]
            tmp_server.lastTimeUpdate = server["lastTimeUpdate"]
            tmp_server.verified = server["verified"]
            tmp_server.promoted = server["promoted"]
            tmp_server.visible = server["visible"]
            tmp_server.hasCustomSkin = server["hasCustomSkin"]
            tmp_server.bannerUrl = server["bannerUrl"]
            tmp_server.address = server["address"]
            tmp_server.group = server["group"]
            return_servers.append(tmp_server)

        return return_servers


def validate_id(server_id: any) -> bool:
    """Validate a server id

    Args:
        server_id (any): The id you want to check.

    Returns:
        bool: True = valid, False = invalid
    """
    if not isinstance(server_id, str):
        return False
    regex = compile(r"^[\da-zA-Z]{7}$")
    result = regex.match(server_id)
    if result is not None:
        return True
    else:
        return False


if __name__ == "__main__":
    print("This is a Module!")
    sys.exit()
