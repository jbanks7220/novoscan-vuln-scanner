import json
import markdown2
from lxml import etree


def export_report(results, file_path):
    if file_path.endswith(".json"):
        with open(file_path, "w") as f:
            json.dump(results, f, indent=4)

    elif file_path.endswith(".md"):
        with open(file_path, "w") as f:
            for r in results:
                f.write(f"- **{r['name']}** ({r['severity']}): {r['description']}\n")

    elif file_path.endswith(".html"):
        md = ""
        for r in results:
            md += f"- **{r['name']}** ({r['severity']}): {r['description']}\n"
        html = markdown2.markdown(md)
        with open(file_path, "w") as f:
            f.write(html)

    elif file_path.endswith(".xml"):
        root = etree.Element("scan_results")
        for r in results:
            v = etree.SubElement(root, "vulnerability")
            etree.SubElement(v, "name").text = r["name"]
            etree.SubElement(v, "severity").text = r["severity"]
            etree.SubElement(v, "description").text = r["description"]
        tree = etree.ElementTree(root)
        tree.write(file_path, pretty_print=True, encoding="utf-8", xml_declaration=True)
