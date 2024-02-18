import toml

# Load and parse the TOML file
with open(
    "/Users/kiran-raga/RagaAI/llm-package/raga-llm-eval/raga_llm_eval/llm_tests/test_details.toml",
    "r",
) as toml_file:
    toml_data = toml.load(toml_file)

output_md_path = "test_description.md"
with open(output_md_path, "w") as md_file:
    for i in range(len(list(toml_data.keys()))):
        # Extract the necessary information
        section_name = list(toml_data.keys())[i]
        section_data = toml_data[section_name]

        # Format the information into Markdown
        markdown_content = f"""### {section_name.replace('_', ' ').title()}\n\n"""
        markdown_content += f"**Description:** {section_data['description']}\n\n"
        markdown_content += "**Expected Arguments:** \n"
        for arg in section_data["expected_arguments"].split(", "):
            markdown_content += f"- `{arg}`\n"
        markdown_content += (
            f"\n**Expected Output:** {section_data['expected_output']}\n\n"
        )
        markdown_content += (
            f"**Interpretation:** {section_data['interpretation']}\n\n---\n"
        )

        # Write the formatted Markdown content to a new .md file
        md_file.write(markdown_content)
