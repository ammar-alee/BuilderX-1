from datatypes import *

from datetime import datetime, timedelta


def generate_trial_end():
    return datetime.now() + timedelta(days=29)


CONFIG = """{
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
    "editor.Component.state": trues
}"""

ANONYMOUS_PIC = "https://previews.123rf.com/images/salamatik/salamatik1803/salamatik180300029/98276437-profile-anonymous-face-icon-gray-silhouette-person-male-businessman-profile-default-avatar-photo-pla.jpg"

USER = User(
    id=1,
    name="Default User",
    email="user@user.com",
    google_id=None,
    google=None,
    created_at=datetime.now(),
    updated_at=datetime.now(),
    isAdmin=False,
    active=1,
    config=CONFIG,
    deleted_at=None,
    activeTeamId=None,
    email_verified_at=None,
    photo_url=ANONYMOUS_PIC,
    uses_two_factor_auth=False,
    current_team_id=1,
    stripe_id=None,
    billing_state=None,
    vat_id=None,
    trial_ends_at=generate_trial_end(),
    last_read_announcements_at=datetime.now(),
    avatar=ANONYMOUS_PIC,
    avatar_original=ANONYMOUS_PIC,
    last_logged_in=datetime.now(),
    newsletter_unsubscribe=0,
    updates_unsubscribe=0,
    disable=0,
    version=1,
    days_remaining=29,

    teams=[1],
)

DOMAIN = Domain(
    _id=1,
    name="gmail.com",
    team_id=1,
    created_at=datetime.now(),
    updated_at=datetime.now()
)

TEAM = Team(
    id=1,
    owner_id=1,
    name="Default Team",
    slug="default.team@gmail.com",
    photo_url=ANONYMOUS_PIC,
    stripe_id=None,
    current_billing_plan=None,
    vat_id=None,
    trial_ends_at=generate_trial_end(),
    created_at=datetime.now(),
    updated_at=datetime.now(),
    disable=0,
    billing_email="",
    extend_trial=1,
    days_remaining=29,
    isSubscribed=1,
    tax_rate=0,
    users=[1],
    domains=[1]
)

PROJECT = Project(
    id=1,
    name="Leet Project 1337",
    userId=USER.id,
    teamId=TEAM.id,
    ownerId=None,
    shareability=0,
    created_at=datetime.now(),
    updated_at=datetime.now(),
    deleted_at=None,
    last_edited_by=None,
    sample=0,
    last_thumbnail_generated_at=datetime.now(),
    last_edited_at=datetime.now(),
    access={
        "access": "write",
        "mode": "design_code"
    },
    isEditable=True
)