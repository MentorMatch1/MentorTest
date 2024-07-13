from config_manager import get_config

# Use configuration values
compatibility_scores = get_config("compatibility_scores", {})
matched_format = get_config("matched_format", {})
mentor_vars = get_config("mentor_vars", [])
mentee_vars = get_config("mentee_vars", [])
cohorts = get_config("cohorts", {})
mentors_matched_data = get_config("mentors_matched_data", {})
