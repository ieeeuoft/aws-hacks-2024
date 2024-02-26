from django.db import models
from django.core import validators
from django.contrib.auth import get_user_model
import uuid

from registration.validators import UploadedFileValidator
from django.core.validators import RegexValidator

User = get_user_model()


def _generate_team_code():
    team_code = uuid.uuid4().hex[:5].upper()
    while Team.objects.filter(team_code=team_code).exists():
        team_code = uuid.uuid4().hex[:5].upper()
    return team_code


class Team(models.Model):
    team_code = models.CharField(max_length=5, default=_generate_team_code, null=False)

    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    MAX_MEMBERS = 4

    def __str__(self):
        return self.team_code


class Application(models.Model):
    GENDER_CHOICES = [
        (None, ""),
        ("male", "Male"),
        ("female", "Female"),
        ("non-binary", "Non-binary"),
        ("other", "Other"),
        ("no-answer", "Prefer not to answer"),
    ]

    PRONOUNS_CHOICES = [
        (None, ""),
        ("she-her", "She/Her"),
        ("he-him", "He/Him"),
        ("they-them", "They/Them"),
        ("she-they", "She/They"),
        ("he-they", "He/They"),
        ("no-answer", "Prefer not to Answer"),
        ("other", "Other"),
    ]

    AGE_CHOICES = [
        (None, ""),
        ("17", "17"),
        ("18", "18"),
        ("19", "19"),
        ("20", "20"),
        ("21", "21"),
        ("22", "22"),
        ("22+", "22+"),
    ]

    ETHNICITY_CHOICES = [
        (None, ""),
        ("asian-indian", "Asian Indian"),
        ("black-african-american", "Black or African American"),
        ("chinese", "Chinese"),
        ("filipino", "Filipino"),
        ("guamanian-chamorro", "Guamanian or Chamorro"),
        ("hispanic-latino", "Hispanic/Latino/Spanish Origin"),
        ("japanese", "Japanese"),
        ("korean", "Korean"),
        ("middle-eastern", "Middle Eastern"),
        ("native-american", "Native American or Alaskan Native"),
        ("native-hawaiian", "Native Hawaiian"),
        ("samoan", "Samoan"),
        ("vietnamese", "Vietnamese"),
        ("caucasian", "White / Caucasian"),
        ("other-asian", "Other Asian (Thai, Cambodian, etc)"),
        ("other-pacific-islander", "Other Pacific Islander"),
        ("other", "Other (please specify)"),
        ("no-answer", "Prefer not to answer"),
    ]

    REFERRAL_CHOICES = [
        (None, ""),
        ("instagram", "Instagram"),
        ("in class/from a professor", "In Class/From a professor"),
        ("discord", "Discord"),
        ("email", "Email"),
        ("from a friend", "From a friend"),
        ("other", "Other"),
    ]

    STUDY_LEVEL_CHOICES = [
        (None, ""),
        ("first-year", "First Year"),
        ("second-year", "Second Year"),
        ("third-year", "Post Doctorate"),
        ("pey", "PEY"),
        ("fourth-year", "Fourth Year"),
        ("grad-school", "Grad School"),
    ]

    PROGRAM_CHOICES = [
        (None, ""),
        ("chemical-engineering", "Chemical Engineering"),
        ("civil-engineering", "Civil Engineering"),
        ("computer-science", "Computer Science"),
        ("electrical-engineering", "Electrical Engineering"),
        ("engineering-science", "Engineering Science"),
        ("industrial-engineering", "Industrial Engineering"),
        ("materials-engineering", "Materials Engineering"),
        ("mineral-engineering", "Mineral Engineering"),
        ("track-one", "TrackOne"),
        ("other", "Other (please specify)"),
    ]

    TSHIRT_SIZE_CHOICES = [
        (None, ""),
        ("S", "S"),
        ("M", "M"),
        ("L", "L"),
        ("XL", "XL"),
    ]

    DIETARY_RESTRICTIONS_CHOICES = [
        (None, ""),
        ("none", "None"),
        ("halal", "Halal"),
        ("vegetarian", "Vegetarian"),
        ("vegan", "Vegan"),
        ("celiac-disease", "Celiac Disease"),
        ("allergies", "Allergies"),
        ("kosher", "Kosher"),
        ("gluten-Free", "Gluten-free"),
        ("other-specify", "Other (please specify)"),
    ]

    YES_NO_UNSURE = [
        (None, ""),
        ("yes", "Yes"),
        ("no", "No"),
        ("unsure", "Unsure"),
    ]

    SEXUALITY = [
        (None, ""),
        ("straight", "Heterosexual or straight"),
        ("gay-lesbian", "Gay or lesbian"),
        ("bisexual", "Bisexual"),
        ("different", "Additional Identity not Listed (Please Specify)"),
        ("no-answer", "Prefer not to answer"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    team = models.ForeignKey(
        Team, related_name="applications", on_delete=models.CASCADE, null=False
    )

    # User Submitted Fields
    age = models.CharField(max_length=50, choices=AGE_CHOICES, null=False)
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES, null=False)
    pronouns = models.CharField(max_length=50, choices=PRONOUNS_CHOICES, null=False)
    ethnicity = models.CharField(max_length=50, choices=ETHNICITY_CHOICES, null=False)
    dietary_restrictions = models.CharField(
        max_length=50, choices=DIETARY_RESTRICTIONS_CHOICES, null=False
    )
    specific_dietary_requirement = models.CharField(max_length=50, blank=True)

    # Address fields
    street_address = models.CharField(
        max_length=255, null=False, help_text="e.g. 35 St George St"
    )
    apt_number = models.CharField(
        max_length=255, null=True, blank=True, help_text="e.g. Apt. No. 13"
    )
    country = models.CharField(max_length=255, null=False)
    city = models.CharField(max_length=255, null=False)
    region = models.CharField(max_length=255, null=False)
    postal_code = models.CharField(max_length=6, null=False)

    student_number = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex="^\d{10}$",
                message="UofT Student number must be exactly 10 digits",
                code="invalid_student_number",
            )
        ],
        help_text="e.g. 1234567890",
    )
    phone_number = models.CharField(
        max_length=20,
        null=False,
        validators=[
            validators.RegexValidator(
                r"^(?:\+\d{1,3})?\s?\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{4}$",
                message="Enter a valid phone number.",
            )
        ],
    )
    study_level = models.CharField(
        max_length=50, choices=STUDY_LEVEL_CHOICES, null=False
    )
    program = models.CharField(max_length=50, choices=PROGRAM_CHOICES, null=False)
    graduation_year = models.IntegerField(
        null=False,
        validators=[
            validators.MinValueValidator(
                2000, message="Enter a realistic graduation year."
            ),
            validators.MaxValueValidator(
                2030, message="Enter a realistic graduation year."
            ),
        ],
    )
    resume = models.FileField(
        upload_to="applications/resumes/",
        validators=[
            UploadedFileValidator(
                content_types=["application/pdf"], max_upload_size=20 * 1024 * 1024
            )
        ],
        null=False,
    )
    linkedin = models.URLField(
        max_length=200, help_text="LinkedIn Profile (Optional)", null=True, blank=True
    )
    github = models.URLField(
        max_length=200, help_text="Github Profile (Optional)", null=True, blank=True
    )
    devpost = models.URLField(
        max_length=200, help_text="Devpost Profile (Optional)", null=True, blank=True
    )
    why_participate = models.TextField(
        null=False,
        help_text="Why do you want to participate in Hack the Student Life?",
        max_length=1000,
    )
    what_technical_experience = models.TextField(
        null=False,
        help_text="What is your technical experience with software and AWS?",
        max_length=1000,
    )
    discovery_method = models.TextField(
        null=False,
        help_text="How did you hear about Hack the Student Life?",
        choices=REFERRAL_CHOICES,
        max_length=100,
    )

    underrepresented_community = models.CharField(
        null=False,
        help_text="Do you identify as a part of an underrepresented group in the technology industry?",
        choices=YES_NO_UNSURE,
        max_length=1000,
    )

    sexual_orientation = models.CharField(
        null=False,
        help_text="Do you consider yourself to be any of the following?",
        choices=SEXUALITY,
        max_length=1000,
    )

    resume_sharing = models.BooleanField(
        help_text="I consent to IEEE UofT sharing my resume with event sponsors.",
        blank=True,
        null=True,
        default=False,
    )
    conduct_agree = models.BooleanField(
        help_text="I have read and agreed to the "
        '<a href="https://aws.amazon.com/codeofconduct/" rel="noopener noreferrer" target="_blank">AWS Code of Conduct</a>.',
        blank=False,
        null=False,
    )

    rsvp = models.BooleanField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    def save(self, *args, **kwargs):
        if (
            self.dietary_restrictions == "other but specify"
            or self.dietary_restrictions == "Other but Specify"
        ):
            self.dietary_restrictions = self.specific_dietary_requirement
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
