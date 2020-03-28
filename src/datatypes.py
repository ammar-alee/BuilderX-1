from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class Domain(object):
    """ What is this object? """
    _id: int
    name: str # Example: gmail.com
    team_id: int
    created_at: datetime
    updated_at: datetime


@dataclass
class Team(object):
    id: int
    owner_id: int
    
    name: str
    slug: str

    # Defaults to a randomly generated photo
    photo_url: str
    
    # What is this
    stripe_id: int # = None
    current_billing_plan: type(None) # = None
    vat_id: type(None) # = None

    # When returned, serialized as yyyy-mm-dd hh:mm:ss
    trial_ends_at: datetime
    created_at: datetime
    updated_at: datetime

    disable: int # = 0
    billing_email: str # = ""
    extend_trial: int # = 0 or 1 ?
    days_remaining: int # between 1 and 7, I guess
    isSubscribed: int # = 1
    tax_rate: int # = 0

    @property
    def pivot(self):
        return {
            "user_id": self.owner_id,
            "team_id": self._id,
            "role": "owner"
        }

    # Serizlized into user/domain jsons without the teams field
    users: List[int] # How STUPID
    domains: List[int]

def serialize_team(self, user=None, domain=None):
    d = self.__dict__.copy()
    if user:
        u = serialize_user(user, None)
        d["users"] = [u]
        d["domains"] = [domain.__dict__]
    return d


@dataclass
class User(object):
    id: int
    email: str
    name: str
    google_id: str # With an integer content, lol
    google: type(None)

    # Serialized the same way as Team::trial_ends_at
    created_at: datetime 
    updated_at: datetime

    isAdmin: bool # Either true or false, not gonna implement admin anyway
    active: int # = 1
    
    # Oh boy
    """
    Contains JSON representation of the following struct:
    {
        "app.tutorial.currentStep": 13,
        "editor.Styling.state": true,
        "editor.layoutEditor.state": true,
        "app.tutorial.skipped": true,
        "editor.overrideEditor.state": true,
        "editor.style.value.int": false,
        "editor.shift.layer.arrow.value": 1,
        "editor.shift.layer.cmd.arrow.value": 5,
        "editor.TextInput.state": true,
        "editor.Device.state": true,
        "editor.Component.state": true
    }
    """
    config: str

    deleted_at: datetime # = None
    activeTeamId: int # ? (= None)
    email_verified_at: datetime # = None
    photo_url: str # From google
    uses_two_factor_auth: bool # = False
    current_team_id: int
    stripe_id: int # = None
    billing_state: type(None)
    vat_id: type(None)
    
    trial_ends_at: datetime # = None
    last_read_announcements_at: datetime # = None
    avatar: str
    avatar_original: str
    last_logged_in: datetime
    
    newsletter_unsubscribe: int # = 0
    updates_unsubscribe: int # = 0
    disable: int # = 0
    version: int # = 1
    days_remaining: int # > 1

    # When served, fully serializes the team too
    teams: List[int]

def serialize_user(self, team=None, domain=None):
    d = self.__dict__.copy()
    if team:
        t = serialize_team(team, self, domain)
        d["teams"] = [t]
        d["currentTeam"] = t
    return d


@dataclass
class File(object):
    id: int
    projectId: str
    name: str

    contentType: str

    # Where is this file stored on the server machine?
    localPath: str

    created_at: datetime
    last_modified: datetime
    deleted_at: datetime
    
    # What are those?
    moved: int
    content_id: int

    def get_size() -> int:
        pass


@dataclass
class Session(object):
    id: int
    project_id: str
    session_id: str
    user_id: int
    last_polled_at: datetime
    created_at: datetime
    updated_at: datetime
    user: object

def create_session(session_id, user, project_id):
    return Session(
        id=1,
        project_id=project_id,
        session_id=session_id,
        user_id=user.id,
        last_polled_at=datetime.now(),
        created_at=datetime.now(),
        updated_at=datetime.now(),
        user=user
    )

def serialize_session(self):
    d = self.__dict__.copy()
    d["user"] = serialize_user(self.user, None, None)
    return d


@dataclass
class Project(object):
    id: str
    userId: str # Representing an int, oh my fucking god
    name: str
    teamId: str
    ownerId: type(None)
    shareability: int # = 0
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime # = None
    last_edited_by: str
    sample: int # = 0
    last_thumbnail_generated_at: datetime
    last_edited_at: datetime
    access: dict
    isEditable: bool # = True

def serialize_project(project, session=None, team=None):
    if team:
        project["team"] = serialize_team(team, None, None)

    if session:
        project["session"] = serialize_session(session)

    return project
