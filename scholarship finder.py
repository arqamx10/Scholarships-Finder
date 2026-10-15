import os
import json
import webbrowser
from datetime import datetime, date

from kivy.app import App
from kivy.metrics import dp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup


# =========================================================
# SCHOLARSHIP DATABASE
# =========================================================

DEFAULT_DATA = [
    {
        "name": "Stipendium Hungaricum",
        "country": "Hungary",
        "level": "Bachelor",
        "field": "Computer Science",
        "minimum_percentage": 70,
        "english_proof": "Varies",
        "funding_type": "Fully Funded",
        "funding": "Tuition + stipend + accommodation contribution",
        "accommodation": "Yes / contribution",
        "deadline": "2027-01-15",
        "status": "Not Started",
        "website": "https://stipendiumhungaricum.hu/apply/"
    },
    {
        "name": "GKS Undergraduate Scholarship",
        "country": "South Korea",
        "level": "Bachelor",
        "field": "Computer Science",
        "minimum_percentage": 80,
        "english_proof": "Varies",
        "funding_type": "Fully Funded",
        "funding": "Tuition + airfare + allowance + other benefits",
        "accommodation": "Allowance",
        "deadline": "Check Official",
        "status": "Not Started",
        "website": "https://www.gks.go.kr/"
    },
    {
        "name": "Türkiye Scholarships",
        "country": "Türkiye",
        "level": "Bachelor",
        "field": "Computer Science",
        "minimum_percentage": 70,
        "english_proof": "Varies",
        "funding_type": "Fully Funded",
        "funding": "Tuition + stipend + accommodation + other support",
        "accommodation": "Yes",
        "deadline": "Check Official",
        "status": "Not Started",
        "website": "https://www.turkiyeburslari.gov.tr/"
    },
    {
        "name": "Romania Government MFA Scholarship",
        "country": "Romania",
        "level": "Bachelor",
        "field": "Computer Science",
        "minimum_percentage": 70,
        "english_proof": "Romanian preparatory year",
        "funding_type": "Fully Funded",
        "funding": "Tuition + monthly scholarship + accommodation support",
        "accommodation": "Student dormitory, subject to places",
        "deadline": "Check Official",
        "status": "Not Started",
        "website": "https://studyinromania.gov.ro/scholarships"
    },
    {
        "name": "MEXT Scholarship",
        "country": "Japan",
        "level": "Bachelor",
        "field": "Computer Science",
        "minimum_percentage": 70,
        "english_proof": "Varies",
        "funding_type": "Fully Funded",
        "funding": "Tuition + monthly allowance + travel support",
        "accommodation": "Allowance",
        "deadline": "Check Official",
        "status": "Not Started",
        "website": "https://www.studyinjapan.go.jp/"
    },
    {
        "name": "Chinese Government Scholarship",
        "country": "China",
        "level": "Bachelor",
        "field": "Computer Science",
        "minimum_percentage": 70,
        "english_proof": "Varies",
        "funding_type": "Fully Funded",
        "funding": "Tuition + accommodation + stipend",
        "accommodation": "Yes",
        "deadline": "Check Official",
        "status": "Not Started",
        "website": "https://www.campuschina.org/"
    },
    {
        "name": "Brunei Government Scholarship",
        "country": "Brunei",
        "level": "Bachelor",
        "field": "Computer Science",
        "minimum_percentage": 70,
        "english_proof": "Varies",
        "funding_type": "Fully Funded",
        "funding": "Tuition + allowances + accommodation",
        "accommodation": "Yes",
        "deadline": "Check Official",
        "status": "Not Started",
        "website": "https://www.mfa.gov.bn/"
    },
    {
        "name": "Azerbaijan Government Scholarship",
        "country": "Azerbaijan",
        "level": "Bachelor",
        "field": "Computer Science",
        "minimum_percentage": 70,
        "english_proof": "Varies",
        "funding_type": "Fully Funded",
        "funding": "Tuition + stipend + medical + travel support",
        "accommodation": "Varies",
        "deadline": "Check Official",
        "status": "Not Started",
        "website": "https://studyinazerbaijan.edu.az/"
    },
    {
        "name": "IsDB Undergraduate Scholarship",
        "country": "International",
        "level": "Bachelor",
        "field": "Computer Science",
        "minimum_percentage": 70,
        "english_proof": "Varies",
        "funding_type": "Fully Funded",
        "funding": "Education and related financial support",
        "accommodation": "Varies",
        "deadline": "Check Official",
        "status": "Not Started",
        "website": "https://www.isdb.org/scholarships"
    },
    {
        "name": "University Merit Scholarship",
        "country": "International",
        "level": "Bachelor",
        "field": "Computer Science",
        "minimum_percentage": 80,
        "english_proof": "Varies",
        "funding_type": "Partial",
        "funding": "Tuition reduction / merit award",
        "accommodation": "Varies",
        "deadline": "Check Official",
        "status": "Not Started",
        "website": "https://www.studyin-europe.eu/"
    }
]


# =========================================================
# BASIC UI HELPERS
# =========================================================

def make_label(text, size=16, height=None):
    label = Label(
        text=str(text),
        font_size=dp(size),
        halign="left",
        valign="middle"
    )
    label.bind(size=lambda obj, value: setattr(obj, "text_size", value))

    if height:
        label.size_hint_y = None
        label.height = dp(height)

    return label


def make_button(text, callback=None, height=48):
    btn = Button(
        text=text,
        font_size=dp(15),
        size_hint_y=None,
        height=dp(height)
    )

    if callback:
        btn.bind(on_release=callback)

    return btn


def make_scroll():
    scroll = ScrollView(
        do_scroll_x=False,
        do_scroll_y=True
    )

    box = BoxLayout(
        orientation="vertical",
        spacing=dp(10),
        padding=dp(12),
        size_hint_y=None
    )

    box.bind(minimum_height=box.setter("height"))

    scroll.add_widget(box)

    return scroll, box


# =========================================================
# BOTTOM NAVIGATION
# =========================================================

def bottom_nav(app):
    nav = BoxLayout(
        size_hint_y=None,
        height=dp(55),
        spacing=dp(4)
    )

    nav.add_widget(
        make_button(
            "Home",
            lambda x: app.go("home")
        )
    )

    nav.add_widget(
        make_button(
            "All",
            lambda x: app.go("all")
        )
    )

    nav.add_widget(
        make_button(
            "Matches",
            lambda x: app.go("matches")
        )
    )

    nav.add_widget(
        make_button(
            "Profile",
            lambda x: app.go("profile")
        )
    )

    nav.add_widget(
        make_button(
            "Tracker",
            lambda x: app.go("tracker")
        )
    )

    return nav


# =========================================================
# HOME SCREEN
# =========================================================

class HomeScreen(Screen):

    def on_pre_enter(self):
        self.refresh()

    def refresh(self):

        app = App.get_running_app()

        self.clear_widgets()

        root = BoxLayout(
            orientation="vertical"
        )

        scroll, box = make_scroll()

        title = make_label(
            "🎓 Scholarship Finder",
            24,
            60
        )
        box.add_widget(title)

        box.add_widget(
            make_label(
                "Find scholarships, check your match score and track applications.",
                15,
                55
            )
        )

        total = len(app.scholarships)

        not_started = len([
            x for x in app.scholarships
            if x.get("status") == "Not Started"
        ])

        applied = len([
            x for x in app.scholarships
            if x.get("status") == "Applied"
        ])

        shortlisted = len([
            x for x in app.scholarships
            if x.get("status") == "Shortlisted"
        ])

        box.add_widget(
            make_label(
                f"Total Scholarships: {total}",
                18,
                45
            )
        )

        box.add_widget(
            make_label(
                f"Not Started: {not_started}",
                16,
                40
            )
        )

        box.add_widget(
            make_label(
                f"Shortlisted: {shortlisted}",
                16,
                40
            )
        )

        box.add_widget(
            make_label(
                f"Applied: {applied}",
                16,
                40
            )
        )

        box.add_widget(
            make_button(
                "🔎 Find My Matches",
                lambda x: app.go("matches"),
                55
            )
        )

        box.add_widget(
            make_button(
                "📚 All Scholarships",
                lambda x: app.go("all"),
                55
            )
        )

        box.add_widget(
            make_button(
                "👤 My Profile",
                lambda x: app.go("profile"),
                55
            )
        )

        box.add_widget(
            make_button(
                "📋 Application Tracker",
                lambda x: app.go("tracker"),
                55
            )
        )

        box.add_widget(
            make_button(
                "📄 Documents Checklist",
                lambda x: app.go("documents"),
                55
            )
        )

        box.add_widget(
            make_button(
                "📅 Deadlines",
                lambda x: app.go("dates"),
                55
            )
        )

        box.add_widget(
            make_button(
                "🔔 Deadline Reminder",
                lambda x: app.check_deadline_reminders(),
                55
            )
        )

        root.add_widget(scroll)
        root.add_widget(bottom_nav(app))

        self.add_widget(root)


# =========================================================
# ALL SCHOLARSHIPS
# =========================================================

class AllScreen(Screen):

    def on_pre_enter(self):
        self.refresh()

    def refresh(self):

        app = App.get_running_app()

        self.clear_widgets()

        root = BoxLayout(
            orientation="vertical"
        )

        scroll, box = make_scroll()

        box.add_widget(
            make_label(
                "📚 All Scholarships",
                23,
                55
            )
        )

        for index, scholarship in enumerate(app.scholarships):

            card = BoxLayout(
                orientation="vertical",
                size_hint_y=None,
                height=dp(135),
                spacing=dp(4)
            )

            card.add_widget(
                make_label(
                    scholarship["name"],
                    18,
                    35
                )
            )

            card.add_widget(
                make_label(
                    f'{scholarship["country"]} • '
                    f'{scholarship["level"]} • '
                    f'{scholarship["funding_type"]}',
                    14,
                    30
                )
            )

            card.add_widget(
                make_label(
                    f'Deadline: {scholarship["deadline"]}',
                    14,
                    28
                )
            )

            card.add_widget(
                make_button(
                    "View Details",
                    lambda x, i=index:
                    app.open_details(i),
                    38
                )
            )

            box.add_widget(card)

        root.add_widget(scroll)
        root.add_widget(bottom_nav(app))

        self.add_widget(root)


# =========================================================
# DETAILS SCREEN
# =========================================================

class DetailsScreen(Screen):

    def show_scholarship(self, index):

        app = App.get_running_app()

        self.index = index
        scholarship = app.scholarships[index]

        self.clear_widgets()

        root = BoxLayout(
            orientation="vertical"
        )

        scroll, box = make_scroll()

        box.add_widget(
            make_label(
                scholarship["name"],
                23,
                65
            )
        )

        details = [
            ("Country", scholarship["country"]),
            ("Level", scholarship["level"]),
            ("Field", scholarship["field"]),
            ("Minimum Percentage",
             str(scholarship["minimum_percentage"]) + "%"),
            ("English Proof", scholarship["english_proof"]),
            ("Funding Type", scholarship["funding_type"]),
            ("Funding", scholarship["funding"]),
            ("Accommodation", scholarship["accommodation"]),
            ("Deadline", scholarship["deadline"]),
            ("Application Status", scholarship["status"])
        ]

        for key, value in details:

            box.add_widget(
                make_label(
                    f"{key}: {value}",
                    15,
                    42
                )
            )

        box.add_widget(
            make_button(
                "🌐 Official Website",
                lambda x:
                app.open_website(scholarship["website"]),
                50
            )
        )

        box.add_widget(
            make_button(
                "🔄 Change Application Status",
                lambda x:
                app.change_status_popup(index),
                50
            )
        )

        box.add_widget(
            make_button(
                "⬅ Back",
                lambda x:
                app.go("all"),
                50
            )
        )

        root.add_widget(scroll)

        self.add_widget(root)


# =========================================================
# SEARCH SCREEN
# =========================================================

class SearchScreen(Screen):

    def on_pre_enter(self):
        self.refresh()

    def refresh(self):

        app = App.get_running_app()

        self.clear_widgets()

        root = BoxLayout(
            orientation="vertical"
        )

        scroll, box = make_scroll()

        search = TextInput(
            hint_text="Search scholarship / country / field",
            multiline=False,
            size_hint_y=None,
            height=dp(50)
        )

        box.add_widget(search)

        result_box = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=dp(8)
        )

        result_box.bind(
            minimum_height=result_box.setter("height")
        )

        box.add_widget(result_box)

        def perform_search(*args):

            result_box.clear_widgets()

            query = search.text.lower().strip()

            for index, s in enumerate(app.scholarships):

                text = (
                    s["name"] + " " +
                    s["country"] + " " +
                    s["field"]
                ).lower()

                if query in text:

                    result_box.add_widget(
                        make_label(
                            s["name"],
                            16,
                            35
                        )
                    )

                    result_box.add_widget(
                        make_button(
                            "Open",
                            lambda x, i=index:
                            app.open_details(i),
                            42
                        )
                    )

        search.bind(text=perform_search)

        root.add_widget(scroll)
        root.add_widget(bottom_nav(app))

        self.add_widget(root)


# =========================================================
# ADVANCED MATCH FILTERS
# =========================================================

class MatchesScreen(Screen):

    def on_pre_enter(self):
        self.refresh()

    def refresh(self):

        app = App.get_running_app()

        self.clear_widgets()

        root = BoxLayout(
            orientation="vertical"
        )

        scroll, box = make_scroll()

        box.add_widget(
            make_label(
                "🎯 Scholarship Matching",
                23,
                55
            )
        )

        countries = ["Any"] + sorted(
            list(set(
                s["country"]
                for s in app.scholarships
            ))
        )

        fields = ["Any"] + sorted(
            list(set(
                s["field"]
                for s in app.scholarships
            ))
        )

        levels = ["Any"] + sorted(
            list(set(
                s["level"]
                for s in app.scholarships
            ))
        )

        funding = ["Any"] + sorted(
            list(set(
                s["funding_type"]
                for s in app.scholarships
            ))
        )

        country_spinner = Spinner(
            text="Any",
            values=countries,
            size_hint_y=None,
            height=dp(48)
        )

        field_spinner = Spinner(
            text="Any",
            values=fields,
            size_hint_y=None,
            height=dp(48)
        )

        level_spinner = Spinner(
            text="Any",
            values=levels,
            size_hint_y=None,
            height=dp(48)
        )

        funding_spinner = Spinner(
            text="Any",
            values=funding,
            size_hint_y=None,
            height=dp(48)
        )

        box.add_widget(
            make_label("Country", 14, 30)
        )
        box.add_widget(country_spinner)

        box.add_widget(
            make_label("Field", 14, 30)
        )
        box.add_widget(field_spinner)

        box.add_widget(
            make_label("Level", 14, 30)
        )
        box.add_widget(level_spinner)

        box.add_widget(
            make_label("Funding", 14, 30)
        )
        box.add_widget(funding_spinner)

        box.add_widget(
            make_label(
                "Your Matching Results",
                19,
                45
            )
        )

        result_box = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=dp(8)
        )

        result_box.bind(
            minimum_height=result_box.setter("height")
        )

        box.add_widget(result_box)

        def apply_filters(*args):

            result_box.clear_widgets()

            results = []

            for index, s in enumerate(app.scholarships):

                if (
                    country_spinner.text != "Any"
                    and s["country"] != country_spinner.text
                ):
                    continue

                if (
                    field_spinner.text != "Any"
                    and s["field"] != field_spinner.text
                ):
                    continue

                if (
                    level_spinner.text != "Any"
                    and s["level"] != level_spinner.text
                ):
                    continue

                if (
                    funding_spinner.text != "Any"
                    and s["funding_type"] != funding_spinner.text
                ):
                    continue

                score = app.calculate_score(s)

                results.append(
                    (score, index, s)
                )

            results.sort(
                key=lambda x: x[0],
                reverse=True
            )

            if not results:

                result_box.add_widget(
                    make_label(
                        "No scholarships match these filters.",
                        15,
                        50
                    )
                )

            for score, index, s in results:

                result_box.add_widget(
                    make_label(
                        f'{s["name"]}\n'
                        f'{s["country"]} • '
                        f'{s["funding_type"]}\n'
                        f'⭐ Match Score: {score}%',
                        15,
                        85
                    )
                )

                result_box.add_widget(
                    make_button(
                        "View Details",
                        lambda x, i=index:
                        app.open_details(i),
                        42
                    )
                )

        apply_button = make_button(
            "🔎 Apply Filters",
            apply_filters,
            52
        )

        box.add_widget(apply_button)

        apply_filters()

        root.add_widget(scroll)
        root.add_widget(bottom_nav(app))

        self.add_widget(root)


# =========================================================
# PERSONAL PROFILE
# =========================================================

class ProfileScreen(Screen):

    def on_pre_enter(self):
        self.refresh()

    def refresh(self):

        app = App.get_running_app()

        self.clear_widgets()

        profile = app.profile

        root = BoxLayout(
            orientation="vertical"
        )

        scroll, box = make_scroll()

        box.add_widget(
            make_label(
                "👤 My Profile",
                23,
                55
            )
        )

        box.add_widget(
            make_label(
                "Enter your information for better scholarship matching.",
                14,
                55
            )
        )

        name_input = TextInput(
            text=profile.get("name", ""),
            hint_text="Name",
            multiline=False,
            size_hint_y=None,
            height=dp(48)
        )

        matric_input = TextInput(
            text=str(profile.get("matric", "")),
            hint_text="Matric Percentage",
            input_filter="float",
            multiline=False,
            size_hint_y=None,
            height=dp(48)
        )

        fsc_input = TextInput(
            text=str(profile.get("fsc", "")),
            hint_text="FSc Percentage",
            input_filter="float",
            multiline=False,
            size_hint_y=None,
            height=dp(48)
        )

        field_spinner = Spinner(
            text=profile.get(
                "field",
                "Computer Science"
            ),
            values=[
                "Computer Science",
                "Engineering",
                "Business",
                "Social Sciences",
                "Natural Sciences",
                "Any"
            ],
            size_hint_y=None,
            height=dp(48)
        )

        english_spinner = Spinner(
            text=profile.get(
                "english",
                "MOI / English Certificate"
            ),
            values=[
                "MOI / English Certificate",
                "IELTS",
                "TOEFL",
                "PTE",
                "None / Not Yet"
            ],
            size_hint_y=None,
            height=dp(48)
        )

        country_input = TextInput(
            text=profile.get("countries", ""),
            hint_text="Preferred countries, e.g. Hungary, Germany",
            multiline=False,
            size_hint_y=None,
            height=dp(48)
        )

        box.add_widget(name_input)
        box.add_widget(matric_input)
        box.add_widget(fsc_input)
        box.add_widget(field_spinner)
        box.add_widget(english_spinner)
        box.add_widget(country_input)

        def save_profile(*args):

            try:
                matric = float(
                    matric_input.text
                ) if matric_input.text else 0

                fsc = float(
                    fsc_input.text
                ) if fsc_input.text else 0

            except ValueError:

                self.show_message(
                    "Please enter valid percentages."
                )

                return

            profile["name"] = name_input.text
            profile["matric"] = matric
            profile["fsc"] = fsc
            profile["field"] = field_spinner.text
            profile["english"] = english_spinner.text
            profile["countries"] = country_input.text

            app.save_profile()

            self.show_message(
                "Profile saved successfully!"
            )

        box.add_widget(
            make_button(
                "💾 Save Profile",
                save_profile,
                55
            )
        )

        box.add_widget(
            make_button(
                "🎯 See My Matches",
                lambda x:
                app.go("matches"),
                55
            )
        )

        root.add_widget(scroll)
        root.add_widget(bottom_nav(app))

        self.add_widget(root)

    def show_message(self, message):

        Popup(
            title="Profile",
            content=make_label(
                message,
                16,
                80
            ),
            size_hint=(0.85, 0.3)
        ).open()


# =========================================================
# MATCH SCORE
# =========================================================

# Score calculation is inside ScholarshipApp


# =========================================================
# APPLICATION TRACKER
# =========================================================

class TrackerScreen(Screen):

    def on_pre_enter(self):
        self.refresh()

    def refresh(self):

        app = App.get_running_app()

        self.clear_widgets()

        root = BoxLayout(
            orientation="vertical"
        )

        scroll, box = make_scroll()

        box.add_widget(
            make_label(
                "📋 Application Tracker",
                23,
                55
            )
        )

        statuses = [
            "Not Started",
            "Shortlisted",
            "Preparing",
            "Applied",
            "Interview",
            "Accepted",
            "Rejected"
        ]

        for index, s in enumerate(app.scholarships):

            box.add_widget(
                make_label(
                    f'{s["name"]}\n'
                    f'Current: {s["status"]}',
                    15,
                    65
                )
            )

            spinner = Spinner(
                text=s["status"],
                values=statuses,
                size_hint_y=None,
                height=dp(45)
            )

            def update_status(
                spinner,
                value,
                i=index
            ):

                app.scholarships[i]["status"] = value
                app.save_data()

            spinner.bind(
                text=update_status
            )

            box.add_widget(spinner)

        root.add_widget(scroll)
        root.add_widget(bottom_nav(app))

        self.add_widget(root)


# =========================================================
# DOCUMENT CHECKLIST
# =========================================================

class DocumentsScreen(Screen):

    DEFAULT_DOCS = [
        "Passport",
        "CNIC / B-Form",
        "Matric Certificate",
        "Matric Transcript",
        "FSc Certificate",
        "FSc Transcript",
        "English Proficiency Proof",
        "CV",
        "Motivation Letter",
        "Recommendation Letter",
        "Passport Photos",
        "Medical Certificate",
        "Police / Character Certificate",
        "Financial Documents",
        "Scholarship Application Form"
    ]

    def on_pre_enter(self):
        self.refresh()

    def refresh(self):

        app = App.get_running_app()

        self.clear_widgets()

        root = BoxLayout(
            orientation="vertical"
        )

        scroll, box = make_scroll()

        box.add_widget(
            make_label(
                "📄 Documents Checklist",
                23,
                55
            )
        )

        box.add_widget(
            make_label(
                "Tap a document button to mark it Ready / Pending.",
                14,
                45
            )
        )

        docs = app.documents

        for doc in self.DEFAULT_DOCS:

            status = docs.get(
                doc,
                False
            )

            text = (
                "✅ " if status else "⬜ "
            ) + doc

            btn = make_button(
                text,
                None,
                48
            )

            def toggle(
                button,
                d=doc
            ):

                app.documents[d] = not app.documents.get(
                    d,
                    False
                )

                app.save_documents()

                self.refresh()

            btn.bind(
                on_release=toggle
            )

            box.add_widget(btn)

        completed = len([
            x for x in docs.values()
            if x
        ])

        total = len(self.DEFAULT_DOCS)

        box.add_widget(
            make_label(
                f"Progress: {completed}/{total} documents ready",
                17,
                50
            )
        )

        root.add_widget(scroll)
        root.add_widget(bottom_nav(app))

        self.add_widget(root)


# =========================================================
# DEADLINES
# =========================================================

class DatesScreen(Screen):

    def on_pre_enter(self):
        self.refresh()

    def refresh(self):

        app = App.get_running_app()

        self.clear_widgets()

        root = BoxLayout(
            orientation="vertical"
        )

        scroll, box = make_scroll()

        box.add_widget(
            make_label(
                "📅 Scholarship Deadlines",
                23,
                55
            )
        )

        scholarships = []

        for index, s in enumerate(app.scholarships):

            deadline = s["deadline"]

            if deadline == "Check Official":

                days = None

            else:

                try:

                    d = datetime.strptime(
                        deadline,
                        "%Y-%m-%d"
                    ).date()

                    days = (
                        d - date.today()
                    ).days

                except:

                    days = None

            scholarships.append(
                (days, index, s)
            )

        scholarships.sort(
            key=lambda x:
            x[0] if x[0] is not None else 99999
        )

        for days, index, s in scholarships:

            if days is None:

                remaining = "Check Official"

            elif days < 0:

                remaining = "Deadline passed"

            elif days == 0:

                remaining = "Due today"

            else:

                remaining = f"{days} days remaining"

            box.add_widget(
                make_label(
                    f'{s["name"]}\n'
                    f'Deadline: {s["deadline"]}\n'
                    f'{remaining}',
                    15,
                    80
                )
            )

            box.add_widget(
                make_button(
                    "View",
                    lambda x, i=index:
                    app.open_details(i),
                    40
                )
            )

        root.add_widget(scroll)
        root.add_widget(bottom_nav(app))

        self.add_widget(root)


# =========================================================
# STATUS SCREEN
# =========================================================

class StatusScreen(Screen):

    def on_pre_enter(self):
        self.refresh()

    def refresh(self):

        app = App.get_running_app()

        self.clear_widgets()

        root = BoxLayout(
            orientation="vertical"
        )

        scroll, box = make_scroll()

        box.add_widget(
            make_label(
                "📊 Application Status",
                23,
                55
            )
        )

        statuses = [
            "Not Started",
            "Shortlisted",
            "Preparing",
            "Applied",
            "Interview",
            "Accepted",
            "Rejected"
        ]

        for status in statuses:

            items = [
                s for s in app.scholarships
                if s["status"] == status
            ]

            box.add_widget(
                make_label(
                    f"{status}: {len(items)}",
                    18,
                    42
                )
            )

            for s in items:

                box.add_widget(
                    make_label(
                        "• " + s["name"],
                        14,
                        35
                    )
                )

        root.add_widget(scroll)
        root.add_widget(bottom_nav(app))

        self.add_widget(root)


# =========================================================
# MAIN APP
# =========================================================

class ScholarshipApp(App):

    def build(self):

        self.title = "Scholarship Finder"

        self.data_file = os.path.join(
            self.user_data_dir,
            "scholarships.json"
        )

        self.profile_file = os.path.join(
            self.user_data_dir,
            "profile.json"
        )

        self.documents_file = os.path.join(
            self.user_data_dir,
            "documents.json"
        )

        self.load_data()
        self.load_profile()
        self.load_documents()

        manager = ScreenManager()

        manager.add_widget(
            HomeScreen(name="home")
        )

        manager.add_widget(
            AllScreen(name="all")
        )

        manager.add_widget(
            DetailsScreen(name="details")
        )

        manager.add_widget(
            SearchScreen(name="search")
        )

        manager.add_widget(
            MatchesScreen(name="matches")
        )

        manager.add_widget(
            ProfileScreen(name="profile")
        )

        manager.add_widget(
            TrackerScreen(name="tracker")
        )

        manager.add_widget(
            DocumentsScreen(name="documents")
        )

        manager.add_widget(
            DatesScreen(name="dates")
        )

        manager.add_widget(
            StatusScreen(name="status")
        )

        return manager

    # =====================================================
    # DATA
    # =====================================================

    def load_data(self):

        if os.path.exists(self.data_file):

            try:

                with open(
                    self.data_file,
                    "r",
                    encoding="utf-8"
                ) as f:

                    self.scholarships = json.load(f)

            except:

                self.scholarships = DEFAULT_DATA.copy()

        else:

            self.scholarships = DEFAULT_DATA.copy()

            self.save_data()

    def save_data(self):

        with open(
            self.data_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.scholarships,
                f,
                indent=4,
                ensure_ascii=False
            )

    # =====================================================
    # PROFILE
    # =====================================================

    def load_profile(self):

        default_profile = {
            "name": "",
            "matric": 0,
            "fsc": 0,
            "field": "Computer Science",
            "english": "MOI / English Certificate",
            "countries": ""
        }

        if os.path.exists(
            self.profile_file
        ):

            try:

                with open(
                    self.profile_file,
                    "r",
                    encoding="utf-8"
                ) as f:

                    self.profile = json.load(f)

            except:

                self.profile = default_profile

        else:

            self.profile = default_profile

    def save_profile(self):

        with open(
            self.profile_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.profile,
                f,
                indent=4,
                ensure_ascii=False
            )

    # =====================================================
    # DOCUMENTS
    # =====================================================

    def load_documents(self):

        if os.path.exists(
            self.documents_file
        ):

            try:

                with open(
                    self.documents_file,
                    "r",
                    encoding="utf-8"
                ) as f:

                    self.documents = json.load(f)

            except:

                self.documents = {}

        else:

            self.documents = {}

    def save_documents(self):

        with open(
            self.documents_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.documents,
                f,
                indent=4,
                ensure_ascii=False
            )

    # =====================================================
    # NAVIGATION
    # =====================================================

    def go(self, screen_name):

        self.root.current = screen_name

    # =====================================================
    # DETAILS
    # =====================================================

    def open_details(self, index):

        screen = self.root.get_screen(
            "details"
        )

        screen.show_scholarship(index)

        self.go("details")

    # =====================================================
    # WEBSITE
    # =====================================================

    def open_website(self, url):

        try:

            webbrowser.open(url)

        except Exception as e:

            self.show_popup(
                "Website Error",
                str(e)
            )

    # =====================================================
    # STATUS
    # =====================================================

    def change_status_popup(self, index):

        statuses = [
            "Not Started",
            "Shortlisted",
            "Preparing",
            "Applied",
            "Interview",
            "Accepted",
            "Rejected"
        ]

        layout = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(10)
        )

        spinner = Spinner(
            text=self.scholarships[index]["status"],
            values=statuses,
            size_hint_y=None,
            height=dp(50)
        )

        save_btn = make_button(
            "Save",
            None,
            50
        )

        layout.add_widget(spinner)
        layout.add_widget(save_btn)

        popup = Popup(
            title="Change Status",
            content=layout,
            size_hint=(0.85, 0.35)
        )

        def save(*args):

            self.scholarships[index]["status"] = spinner.text

            self.save_data()

            popup.dismiss()

            self.root.get_screen(
                "home"
            ).refresh()

        save_btn.bind(
            on_release=save
        )

        popup.open()

    # =====================================================
    # MATCH SCORE
    # =====================================================

    def calculate_score(self, scholarship):

        score = 0

        profile = self.profile

        # Academic score
        academic = max(
            profile.get("matric", 0),
            profile.get("fsc", 0)
        )

        minimum = scholarship.get(
            "minimum_percentage",
            0
        )

        if academic >= minimum:

            score += 35

        elif academic >= minimum - 5:

            score += 20

        # Field
        preferred_field = profile.get(
            "field",
            ""
        )

        if (
            preferred_field == "Any"
            or preferred_field == scholarship["field"]
        ):

            score += 25

        # Level
        if scholarship["level"] == "Bachelor":

            score += 15

        # Funding
        if scholarship["funding_type"] == "Fully Funded":

            score += 15

        else:

            score += 5

        # Country preference
        countries = profile.get(
            "countries",
            ""
        ).lower()

        if countries:

            if scholarship["country"].lower() in countries:

                score += 10

        else:

            score += 5

        return min(
            score,
            100
        )

    # =====================================================
    # DEADLINE REMINDER
    # =====================================================

    def check_deadline_reminders(self):

        upcoming = []

        for s in self.scholarships:

            deadline = s["deadline"]

            if deadline == "Check Official":

                continue

            try:

                d = datetime.strptime(
                    deadline,
                    "%Y-%m-%d"
                ).date()

                days = (
                    d - date.today()
                ).days

                if 0 <= days <= 30:

                    upcoming.append(
                        f'{s["name"]}: {days} days remaining'
                    )

            except:

                pass

        if upcoming:

            message = "\n".join(
                upcoming
            )

        else:

            message = (
                "No saved deadline is within "
                "the next 30 days.\n\n"
                "For scholarships marked "
                "\"Check Official\", visit the "
                "official website."
            )

        self.show_popup(
            "🔔 Deadline Reminder",
            message
        )

    # =====================================================
    # POPUP
    # =====================================================

    def show_popup(
        self,
        title,
        message
    ):

        content = BoxLayout(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(10)
        )

        content.add_widget(
            make_label(
                message,
                15,
                150
            )
        )

        close = make_button(
            "OK",
            None,
            45
        )

        content.add_widget(close)

        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.9, 0.5)
        )

        close.bind(
            on_release=popup.dismiss
        )

        popup.open()

    # =====================================================
    # STARTUP REMINDER
    # =====================================================

    def on_start(self):

        # Small delay is not required.
        # Just keep app startup clean.
        pass


# =========================================================
# RUN APP
# =========================================================

if __name__ == "__main__":
    ScholarshipApp().run()