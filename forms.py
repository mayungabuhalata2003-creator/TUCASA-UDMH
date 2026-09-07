from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    TextAreaField,
    SelectField,
    DateField,
    SubmitField,
)
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional


class SignupForm(FlaskForm):
    jina = StringField("Jina Kamili", validators=[DataRequired(), Length(min=2, max=150)])
    email = StringField("Barua Pepe", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Nywila", validators=[DataRequired(), Length(min=6, message="Nywila iwe na herufi 6 au zaidi")]
    )
    confirm_password = PasswordField(
        "Thibitisha Nywila",
        validators=[DataRequired(), EqualTo("password", message="Nywila hazifanani")],
    )
    submit = SubmitField("Jisajili")


class LoginForm(FlaskForm):
    email = StringField("Username / Barua Pepe", validators=[DataRequired()])
    password = PasswordField("Nywila", validators=[DataRequired()])
    submit = SubmitField("Ingia")


class MemberRegistrationForm(FlaskForm):
    jina = StringField("Jina Kamili", validators=[DataRequired(), Length(min=2, max=150)])
    jinsia = SelectField(
        "Jinsia", choices=[("Me", "Me (Male)"), ("Ke", "Ke (Female)")], validators=[DataRequired()]
    )
    mwaka = SelectField(
        "Mwaka wa Masomo",
        choices=[
            ("Mwaka wa 1", "Mwaka wa 1"),
            ("Mwaka wa 2", "Mwaka wa 2"),
            ("Mwaka wa 3", "Mwaka wa 3"),
            ("Mwaka wa 4", "Mwaka wa 4"),
            ("Uzamili/PhD", "Uzamili/PhD"),
        ],
        validators=[DataRequired()],
    )
    kozi = StringField("Kozi", validators=[DataRequired(), Length(max=150)])
    simu = StringField("Namba ya Simu", validators=[DataRequired(), Length(min=9, max=20)])
    email = StringField("Barua Pepe", validators=[DataRequired(), Email()])
    hostel = StringField("Hostel", validators=[DataRequired(), Length(max=100)])
    tarehe_ya_kuzaliwa = DateField("Tarehe ya Kuzaliwa", format="%Y-%m-%d", validators=[DataRequired(message="Tafadhali weka tarehe yako ya kuzaliwa")])
    vipaji = TextAreaField("Vipaji", validators=[Optional(), Length(max=255)])
    kukubali_whatsapp = BooleanField("Nakubali kupokea ujumbe wa WhatsApp")
    submit = SubmitField("Sajili")


class AnnouncementForm(FlaskForm):
    title = StringField("Kichwa cha Habari", validators=[DataRequired(), Length(max=200)])
    content = TextAreaField("Maudhui", validators=[DataRequired()])
    submit = SubmitField("Hifadhi")


class ContactForm(FlaskForm):
    jina = StringField("Jina Kamili", validators=[DataRequired(), Length(max=150)])
    email = StringField("Barua Pepe", validators=[DataRequired(), Email()])
    ujumbe = TextAreaField("Ujumbe", validators=[DataRequired()])
    submit = SubmitField("Tuma Ujumbe")


class ChatMessageForm(FlaskForm):
    message = TextAreaField(
        "Ujumbe",
        validators=[DataRequired(), Length(max=1000)],
        render_kw={"rows": 2, "maxlength": 1000, "placeholder": "Andika ujumbe wako..."},
    )
    submit = SubmitField("Tuma")


class LogoUploadForm(FlaskForm):
    logo = FileField(
        "Chagua Nembo (Logo)",
        validators=[FileAllowed(["png", "jpg", "jpeg", "gif", "webp"], "Picha pekee zinaruhusiwa!")],
    )
    submit = SubmitField("Pakia Nembo")


class WhatsAppBroadcastForm(FlaskForm):
    message = TextAreaField("Andika Ujumbe", validators=[DataRequired()])
    submit = SubmitField("Tengeneza Viungo vya WhatsApp")


class SettingsForm(FlaskForm):
    association_name = StringField("Jina la Chama/Association", validators=[Optional(), Length(max=200)])
    hostel_name = StringField("Jina la Hostel", validators=[Optional(), Length(max=200)])
    whatsapp_link = StringField("Kiungo cha Kikundi cha WhatsApp", validators=[Optional(), Length(max=500)])
    contact_email = StringField("Barua Pepe ya Mawasiliano", validators=[Optional(), Email(), Length(max=200)])
    submit = SubmitField("Hifadhi Mipangilio")


class LibraryItemForm(FlaskForm):
    title = StringField("Jina la Kitabu/Nyaraka", validators=[DataRequired(), Length(max=200)])
    category = SelectField("Kategoria", choices=[
        ("Ellen G. White", "Ellen G. White"),
        ("Bible", "Bible"),
        ("SDA Hymns", "SDA Hymns"),
        ("Nyingine", "Nyingine"),
    ], validators=[DataRequired()])
    language = SelectField("Lugha", choices=[("Kiswahili", "Kiswahili"), ("English", "English")], validators=[DataRequired()])
    author = StringField("Mwandishi", validators=[Optional(), Length(max=150)])
    resource_url = StringField("Kiungo cha kusoma/kupakua", validators=[Optional(), Length(max=500)])
    file = FileField("PDF ya kitabu (hiari)", validators=[Optional(), FileAllowed(["pdf"], "PDF pekee inaruhusiwa!")])
    submit = SubmitField("Ongeza Library")


class EventPostForm(FlaskForm):
    title = StringField("Kichwa cha Tukio", validators=[DataRequired(), Length(max=200)])
    description = TextAreaField("Maelezo", validators=[DataRequired()])
    event_date = DateField("Tarehe ya Tukio", format="%Y-%m-%d", validators=[Optional()])
    image = FileField("Picha ya Tukio (hiari)", validators=[Optional(), FileAllowed(["png", "jpg", "jpeg", "gif", "webp"], "Picha pekee zinaruhusiwa!")])
    submit = SubmitField("Hifadhi Tukio")


class PublicationForm(FlaskForm):
    title = StringField("Kichwa cha Machapisho", validators=[DataRequired(), Length(max=200)])
    author = StringField("Mwandishi", validators=[Optional(), Length(max=150)])
    summary = TextAreaField("Muhtasari", validators=[Optional()])
    resource_url = StringField("Kiungo cha Njia ya Nje (hiari)", validators=[Optional(), Length(max=500)])
    file = FileField("Faili la PDF/DOCX (hiari)", validators=[Optional(), FileAllowed(["pdf", "doc", "docx"], "Faili la PDF/DOCX pekee linaruhusiwa!")])
    submit = SubmitField("Hifadhi Machapisho")


class ChoirMediaForm(FlaskForm):
    title = StringField("Jina la nyimbo/video/audio", validators=[DataRequired(), Length(max=200)])
    media_type = SelectField(
        "Aina ya media",
        choices=[
            ("song", "Wimbo"),
            ("audio", "Audio"),
            ("video", "Video"),
            ("pdf", "PDF"),
            ("other", "Nyingine"),
        ],
        validators=[DataRequired()],
    )
    description = TextAreaField("Maelezo", validators=[Optional()])
    external_url = StringField("Kiungo cha YouTube/Google Drive (hiari)", validators=[Optional(), Length(max=500)])
    file = FileField("Faili la media (hiari)", validators=[Optional(), FileAllowed(["mp3", "wav", "m4a", "mp4", "mov", "avi", "pdf", "doc", "docx", "png", "jpg", "jpeg", "webp"], "Faili la media linaruhusiwa!")])
    submit = SubmitField("Hifadhi Media")


class WorshipScheduleForm(FlaskForm):
    year = StringField("Mwaka", validators=[DataRequired(), Length(min=4, max=4)])
    day = StringField("Siku", validators=[DataRequired(), Length(max=50)])
    time = StringField("Muda", validators=[DataRequired(), Length(max=50)])
    activity = StringField("Shughuli ya Ibada", validators=[DataRequired(), Length(max=200)])
    submit = SubmitField("Hifadhi Ratiba")


class LeaderForm(FlaskForm):
    year = StringField("Mwaka wa uongozi", validators=[DataRequired(), Length(min=4, max=4)])
    name = StringField("Jina la kiongozi", validators=[DataRequired(), Length(max=150)])
    position = StringField("Cheo", validators=[DataRequired(), Length(max=150)])
    photo = FileField("Picha (hiari)", validators=[Optional(), FileAllowed(["png", "jpg", "jpeg", "webp"], "Picha pekee zinaruhusiwa!")])
    submit = SubmitField("Ongeza Kiongozi")
