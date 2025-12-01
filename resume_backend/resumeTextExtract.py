import pypdf
import re

_SKILLS_TEMPLATE = {
    "Web & Programming": [],
    "Framework & Tools": [],
    "Infrastructure": [],
}
_EXPERIENCE_TEMPLATE = [
    {
        "Title": "",
        "Company": "",
        "Start Date": "",
        "End Date": "",
        "Responsibilities": [],
    }
]
_EDUCATION_TEMPLATE = {
    "University": "",
    "Location": "",
    "Degree": "",
    "Field of Study": "",
    "GPA": "",
}


class Resume:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.sections = {
            "OBJECTIVE": None,
            "SKILLS": None,
            "EXPERIENCE": None,
            "EDUCATION": None,
        }
        self.text = self.extract_text()

    def remove_extra_newlines(self, text):
        # Replace multiple newlines with a single newline
        import re

        return re.sub(r"\n+", "\n", text).strip()

    def format_section(self, section_name, section_text):
        self.remove_extra_newlines(section_text)

        match section_name:
            case "SKILLS":
                for category in _SKILLS_TEMPLATE.keys():
                    if category in section_text:
                        skills_text = section_text.split(category)[1]
                        next_categories = [
                            cat for cat in _SKILLS_TEMPLATE.keys() if cat != category
                        ]
                        for next_cat in next_categories:
                            if next_cat in skills_text:
                                skills_text = skills_text.split(next_cat)[0][2:]
                                print(skills_text)
                        skills_list = [
                            skill.strip(",")
                            for skill in skills_text.split("\n")
                            if skill.strip()
                        ]
                        _SKILLS_TEMPLATE[category] = skills_list
                return _SKILLS_TEMPLATE
            case "EXPERIENCE":
                experiences = []
                job_titles = [
                    "Fullstack Engineer",
                    "Software Engineer",
                    "Data Developer",
                ]

                # Split the section by job titles to get individual experiences
                job_sections = []
                current_text = section_text

                for title in job_titles:
                    if title in current_text:
                        parts = current_text.split(title)
                        if len(parts) > 1:
                            job_sections.append((title, parts[1]))
                            current_text = parts[1]

                for title, job_text in job_sections:
                    experience = {
                        "Title": title,
                        "Company": "",
                        "Start Date": "",
                        "End Date": "",
                        "Responsibilities": [],
                    }

                    lines = [
                        line.strip() for line in job_text.split("\n") if line.strip()
                    ]

                    if lines:
                        # First line should contain Company, Start Date, End Date
                        first_line = lines[0]
                        # Parse the first line to extract company and dates
                        # This assumes format like "Company | Start Date - End Date"
                        if "|" in first_line:
                            parts = first_line.split("-")
                            experience["Company"] = parts[0].strip()
                            if len(parts) > 1 and "-" in parts[1]:
                                dates = parts[1].split("-")
                                experience["Start Date"] = dates[0].strip()
                                experience["End Date"] = (
                                    dates[1].strip() if len(dates) > 1 else ""
                                )

                        # Remaining lines are responsibilities (bullet points)
                        for line in lines[1:]:
                            # Check if this line is the start of a new job title
                            if any(job_title in line for job_title in job_titles):
                                break
                            # Remove bullet point characters if present
                            cleaned_line = line.lstrip("•●○◦-*").strip()
                            if cleaned_line:
                                experience["Responsibilities"].append(cleaned_line)

                    experiences.append(experience)

                return experiences if experiences else _EXPERIENCE_TEMPLATE
            case "EDUCATION":
                education_entries = []
                lines = [
                    line.strip() for line in section_text.split("\n") if line.strip()
                ]

                # Join all lines and split by GPA pattern (ends with a digit)
                full_text = " ".join(lines)

                # Split entries by finding GPA patterns (typically end with a number)
                # Look for patterns like "GPA: 3.5" or just numbers that indicate GPA end
                entries = re.split(r"(\d+\.?\d*)\s+(?=[A-Z])", full_text)

                # Reconstruct entries by pairing splits
                edu_entries_raw = []
                i = 0
                while i < len(entries):
                    if i + 1 < len(entries) and entries[i].strip():
                        # Combine text with its GPA
                        edu_entries_raw.append(
                            entries[i].strip() + " " + entries[i + 1].strip()
                        )
                        i += 2
                    else:
                        if entries[i].strip():
                            edu_entries_raw.append(entries[i].strip())
                        i += 1

                # If no splits found, treat entire text as one entry
                if not edu_entries_raw:
                    edu_entries_raw = [full_text]

                for entry in edu_entries_raw:
                    education = {
                        "University": "",
                        "Location": "",
                        "Degree": "",
                        "Field of Study": "",
                        "GPA": "",
                    }

                    # Extract GPA (last number in the entry)
                    gpa_match = re.search(r"(\d+\.?\d*)$", entry.strip())
                    if gpa_match:
                        education["GPA"] = gpa_match.group(1)
                        entry = entry[: gpa_match.start()].strip()

                    # Split remaining text by common delimiters
                    parts = re.split(r"[,|]|    ", entry)
                    parts = [p.strip() for p in parts if p.strip()]

                    if len(parts) >= 1:
                        education["University"] = parts[0]
                    if len(parts) >= 2:
                        education["Location"] = parts[1] + ", " + parts[2]
                    if len(parts) >= 3:
                        # Check if it contains degree keywords
                        if any(
                            deg in parts[3].lower()
                            for deg in ["bachelor", "master", "bs", "ms", "ba", "ma"]
                        ):
                            education["Degree"] = parts[3]
                        else:
                            education["Field of Study"] = parts[3]
                    if len(parts) >= 4:
                        education["Field of Study"] = parts[4]

                    education_entries.append(education)

                return education_entries if education_entries else [_EDUCATION_TEMPLATE]
        return section_text

    def extract_text(self):
        reader = pypdf.PdfReader(self.pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"

        for section in self.sections.keys():
            keys = list(self.sections.keys())
            current_index = keys.index(section)

            if current_index < len(keys) - 1:
                # Get text between current section and next section
                next_section = keys[current_index + 1]
                self.sections[section] = self.format_section(
                    section, text.split(section)[1].split(next_section)[0].strip()
                )
            else:
                # For the last section, get everything after it
                self.sections[section] = self.format_section(
                    section, text.split(section)[1].strip()
                )
        return self.sections
