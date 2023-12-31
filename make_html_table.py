from typing import Dict, List, Tuple, Set, Iterable, Callable, Collection, Any
from multiple_day_assignments import Day, DayInfo
import jinja2

def make_html_table(multiple_day_assignments: Dict[Day, Dict[str, str]], rides: List[str], html_path: str) -> None:
    template_loader = jinja2.FileSystemLoader(searchpath="./")
    template_env = jinja2.Environment(loader=template_loader)
    template_path = "template.html"
    template = template_env.get_template(template_path)
    output_text = template.render({
        'multiple_day_assignments': multiple_day_assignments,
        'rides': rides
    })
    with open(html_path, 'w') as f:
        f.write(output_text)
