"""
Module for report creation for saved records of user.
"""
import jinja2
import pdfkit
from matplotlib import pyplot as plt
from PIL import Image

from budget_bot_2.custom_exeptions import RequestNotSuccessError
from budget_bot_2.db_connection import Session
from budget_bot_2.repositories import OutcomeRepository
from settings import settings

TEMPLATE_DIR = settings.BASE_DIR.joinpath("jinja_templates")
CSS_PATH = settings.BASE_DIR.joinpath("css", "report.css")
CHARTS_DIR = settings.BASE_DIR.joinpath("charts")
REPORT_PATH = settings.BASE_DIR.joinpath("reports", "report.pdf")

COLORS = [
    "#FFA500",
    "#FF0000",
    "#00FF00",
    "#0000FF",
    "#FFFF00",
    "#87CEFA",
    "#FF00FF",
    "#C0C0C0",
    "#808080",
    "#800000",
    "#808000",
    "#008000",
    "#800080",
    "#008080",
    "#000080",
    "#008000",
]


async def create_report(user_id: int, period: int) -> str:
    """
    Create a report of saved records for user.

    Save report on disk as pdf file
    and return an absotule path of created file.
    Args:
     - user_id - telegram id of user;
     - period - time interval in days for report apart
        form current date.
    """
    async with Session() as session:
        repo = OutcomeRepository(session)
        data_by_categories = await repo.get_grouped_by_categories(
            user_id=user_id, period=period
        )
        if len(data_by_categories) == 0:
            raise RequestNotSuccessError("Нет записей для создания отчета.")
        data_by_days = await repo.get_grouped_by_day(user_id=user_id, period=period)
        ungrouped_data = await repo.get_ungrouped(user_id=user_id, period=period)
    await create_plot(data=[row[1] for row in data_by_categories])
    await create_bar_plot(data=data_by_days)
    html = await render_template(data_by_categories, data_by_days, ungrouped_data)
    pdfkit.from_string(
        html,
        REPORT_PATH,
        options={
            "margin-left": "5",
            "margin-right": "5",
            "margin-bottom": "30",
            "enable-local-file-access": "",
            "quiet": "",
            "encoding": "UTF-8",
            "user-style-sheet": CSS_PATH,
        },
        css=CSS_PATH,
        verbose=True,
    )
    return REPORT_PATH


async def create_plot(data: list[float]) -> None:
    """
    Create a pie plot for a report
     and save it on disk.
    """
    fig, axes = plt.subplots()
    axes.pie(data, colors=COLORS)
    path = CHARTS_DIR.joinpath("fig.jpeg")
    fig.savefig(path)
    with Image.open(path) as image:
        image = image.crop((150, 80, 500, 400))
        image.save(path, "jpeg", quality=100)


async def create_bar_plot(data: list[float]) -> None:
    """
    Create a bar plot for a report
     and save it on disk.
    """
    fig, axes = plt.subplots()
    dates = [row[0].strftime("%d.%m.%y") for row in data]
    amounts = [row[1] for row in data]
    axes.bar(dates, amounts)
    axes.tick_params(axis="x", rotation=50, labelsize=8)
    path = CHARTS_DIR.joinpath("bar_fig.jpeg")
    fig.savefig(CHARTS_DIR.joinpath(path))
    with Image.open(path) as image:
        image = image.resize((500, 400))
        image = image.crop((0, 40, 500, 400))
        image.save(path, "jpeg", quality=100)


async def render_template(
    data_by_categories: list, data_by_days: list, data_ungrouped: list
) -> str:
    """
    Create a html from templates and passed
     sets of data using jinja engine.
     Return it as a string.
    """
    template_loader = jinja2.FileSystemLoader(TEMPLATE_DIR)
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template("basic_template.html")
    data_by_categories.append(("Итого", sum((row[1] for row in data_by_categories))))
    data_by_days.append(("Итого", sum((row[1] for row in data_by_days))))
    data_ungrouped.append(("Итого", "", sum((row[2] for row in data_ungrouped))))
    context = {
        "data_by_categories": data_by_categories,
        "data_by_days": data_by_days,
        "data_ungrouped": data_ungrouped,
        "colors": COLORS,
        "css_path": CSS_PATH,
        "charts_dir": CHARTS_DIR,
    }
    output_text = template.render(context)
    return output_text
