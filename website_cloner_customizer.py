from pywebcopy import save_website
from bs4 import BeautifulSoup
import os
import shutil

def clone_website(url, project_folder):
    """Clone a website to a local folder using PyWebCopy."""
    try:
        save_website(
            url=url,
            project_folder=project_folder,
            project_name="cloned_site",
            bypass_robots=True,  # Respect robots.txt in production
            debug=False,
            open_in_browser=False,
            delay=None,  # Adjust for rate-limiting if needed
            threaded=True  # Faster downloads
        )
        print(f"Successfully cloned {url} to {project_folder}/cloned_site")
    except Exception as e:
        print(f"Error cloning website: {e}")

def customize_website(project_folder, customizations):
    """Customize cloned website files (e.g., change text, styles, or inject scripts)."""
    output_folder = os.path.join(project_folder, "cloned_site")
    
    # Walk through cloned files
    for root, _, files in os.walk(output_folder):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                try:
                    # Read HTML file
                    with open(file_path, "r", encoding="utf-8") as f:
                        soup = BeautifulSoup(f, "html.parser")

                    # Apply customizations
                    for customization in customizations:
                        if customization["type"] == "text":
                            # Replace text in specific tags
                            for tag in soup.find_all(customization["tag"]):
                                if customization["match"] in tag.get_text():
                                    tag.string = customization["new_text"]
                        elif customization["type"] == "style":
                            # Update CSS styles
                            for tag in soup.find_all("style"):
                                tag.string = tag.get_text().replace(
                                    customization["match"], customization["new_style"]
                                )
                        elif customization["type"] == "script":
                            # Inject a script (e.g., analytics)
                            script_tag = soup.new_tag("script")
                            script_tag.string = customization["script_content"]
                            soup.head.append(script_tag)

                    # Save modified HTML
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(str(soup))
                    print(f"Customized {file_path}")
                except Exception as e:
                    print(f"Error customizing {file_path}: {e}")

def main():
    # Configuration
    target_url = "https://example.com"  # Replace with target website
    project_folder = "./cloned_website"  # Local folder for cloned files

    # Define customizations (extend as needed for your SaaS)
    customizations = [
        {
            "type": "text",
            "tag": "h1",
            "match": "Example Domain",
            "new_text": "My SaaS Cloned Site"
        },
        {
            "type": "style",
            "match": "body {",
            "new_style": "body { background-color: #f0f8ff; color: #333; "
        },
        {
            "type": "script",
            "script_content": "console.log('Custom analytics script injected!');"
        }
    ]

    # Clone the website
    clone_website(target_url, project_folder)

    # Customize the cloned files
    customize_website(project_folder, customizations)

    print("Cloning and customization complete!")

if __name__ == "__main__":
    main()
