import logging
from datetime import datetime
from pathlib import Path
from typing import Union
import copy

import dateutil.parser as dparse
from dateutil.parser import ParserError

import gantt_project_maker.gantt as gantt
from gantt_project_maker.colors import color_to_hex
from gantt_project_maker.excelwriter import write_planning_to_excel

SCALES = dict(
    daily=gantt.DRAW_WITH_DAILY_SCALE,
    weekly=gantt.DRAW_WITH_WEEKLY_SCALE,
    monthly=gantt.DRAW_WITH_MONTHLY_SCALE,
    quarterly=gantt.DRAW_WITH_QUARTERLY_SCALE,
)

_logger = logging.getLogger(__name__)


def get_nearest_saturday(date):
    """
    Get the nearest Saturday with respect to 'date'

    Parameters
    ----------
    date: datetime.date
        The reference date

    Returns
    -------
    datetime.date
        Nearest Saturday with respect to the reference date

    """
    d = date.toordinal()
    last = d - 6
    sunday = last - (last % 7)
    saturday = sunday + 6
    if d - saturday > 7 / 2:
        # de afstand tot vorige zaterdag is meer dan een halve week, dus de volgende zaterdag is dichter bij
        saturday += 7
    return date.fromordinal(saturday)


def parse_date(
    date_in: Union[str, datetime], date_default: str = None, dayfirst=False
) -> datetime.date:
    """
    Lees de date_string en parse de datum

    Parameters
    ----------
    date_in: str
        Datum representatie
    date_default:
        Als de date_string None is deze default waarde genomen.
    dayfirst: bool
        Set the day first, e.g. 25-12-2023

    Returns
    -------
    datetime.date():
        Datum
    """
    if date_in is not None:
        try:
            date_out = dparse.parse(date_in.strip(), dayfirst=dayfirst).date()
        except AttributeError:
            # assume the date string is given as a datetime already
            date_out = date_in
    elif date_default is not None and isinstance(date_default, str):
        date_out = dparse.parse(date_default.strip(), dayfirst=dayfirst).date()
    else:
        date_out = date_default
    return date_out


def add_vacation_employee(employee: gantt.Resource, vacations: dict) -> dict:
    """
    Add the vacations of an employee

    Parameters
    ----------
    employee: gannt.Resource
        The employee for who you want to add the vacation
    vacations: dict
        A dictionary with items per vacation. Per vacation, you need a start and an end

    Returns
    -------
    dict:
        Dictionary with the vacations.
    """
    vacation_objects = dict()

    if vacations is not None:
        for vacation_key, vacation_properties in vacations.items():
            vacation_objects[vacation_key] = Vacation(
                vacation_properties["start"],
                vacation_properties.get("end"),
                employee=employee,
            )
    return vacation_objects


class StartEndBase:
    """
    Basis van alle classes met een begin- en einddatum.
    """

    def __init__(self, start: str, end: str = None, dayfirst=False):
        """
        Sla de datum stings op als datetime objecten

        Parameters
        ----------
        start: str
            Start date is mandatory
        end: str or None
            End date is optional.
        dayfirst: bool
            Use date with date first
        """
        self.start = parse_date(start, dayfirst=dayfirst)
        self.end = parse_date(end, dayfirst=dayfirst)


class Vacation(StartEndBase):
    def __init__(self, start, end=None, employee=None, dayfirst=False):
        super().__init__(start, end, dayfirst=dayfirst)

        if employee is None:
            self.pool = gantt
        else:
            self.pool = employee

        self.add_vacation()

    def add_vacation(self):
        """
        Add common or employee vacations
        """
        self.pool.add_vacations(self.start, self.end)


class Employee:
    def __init__(self, label, full_name=None, vacations=None, color=None):
        self.label = label
        self.full_name = full_name
        self.color = color
        self.resource = gantt.Resource(name=label, fullname=full_name, color=color)

        if vacations is not None:
            self.vacations = add_vacation_employee(
                employee=self.resource, vacations=vacations
            )
        else:
            self.vacations = None


class BasicElement(StartEndBase):
    def __init__(
        self,
        label,
        start=None,
        dependent_of=None,
        color=None,
        project_color=None,
        detail=False,
        display=True,
        dayfirst=False,
    ):
        super().__init__(start, start, dayfirst)
        if label is None:
            raise ValueError("Every task should have a label!")
        self.label = label
        self.detail = detail
        self.dependent_of = dependent_of
        self.color = color_to_hex(color)
        self.project_color = color_to_hex(project_color)
        self.display = display


class Task(BasicElement):
    def __init__(
        self,
        label,
        start=None,
        end=None,
        duration=None,
        employees=None,
        dependent_of=None,
        color=None,
        project_color=None,
        detail=False,
        display=True,
        dayfirst=True,
    ):
        super().__init__(
            label=label,
            start=start,
            dependent_of=dependent_of,
            color=color,
            project_color=project_color,
            detail=detail,
            display=display,
            dayfirst=dayfirst,
        )
        self.end = parse_date(end, dayfirst=dayfirst)
        self.duration = duration
        if self.end is None and self.duration is None:
            msg = (
                f"For a Task, next to a start date, either a end date or a duration needs to be specified. "
                f"None is given for task '{label}'"
            )
            raise ValueError(msg)
        if self.end is not None:
            if self.end < self.start:
                msg = f"End date {self.end} is before {self.start} for Task '{label}'. Please fix this"
                raise ValueError(msg)
        self.employees = employees

        self.element = self.add_task()

    def add_task(self) -> gantt.Task:
        if self.color is None:
            self.color = self.project_color
        task = gantt.Task(
            name=self.label,
            start=self.start,
            stop=self.end,
            duration=self.duration,
            depends_of=self.dependent_of,
            resources=self.employees,
            color=self.color,
        )
        return task


class Milestone(BasicElement):
    def __init__(
        self,
        label,
        start=None,
        dependent_of=None,
        color=None,
        project_color=None,
        detail=False,
        display=True,
        dayfirst=True,
    ):
        super().__init__(
            label=label,
            start=start,
            dependent_of=dependent_of,
            color=color,
            project_color=project_color,
            detail=detail,
            display=display,
            dayfirst=dayfirst,
        )

        self.element = self.add_milestone()

    def add_milestone(self) -> gantt.Milestone:
        element = gantt.Milestone(
            name=self.label,
            start=self.start,
            depends_of=self.dependent_of,
            color=self.color,
        )
        return element


class ProjectPlanner:
    def __init__(
        self,
        programma_title: str = None,
        vacations_title: str = None,
        programma_color: str = None,
        vacation_color: str = None,
        output_file_name: Path = None,
        planning_start: datetime = None,
        planning_end: datetime = None,
        weeks_margin_left: int = None,
        weeks_margin_right: int = None,
        today: datetime = None,
        dayfirst: bool = False,
        scale: str = None,
        period_info: dict = None,
        excel_info: dict = None,
        details: bool = None,
        filter_employees: list = None,
        save_svg_as_pdf: bool = False,
        collaps_tasks: bool = False,
        periods: list = None,
    ):
        """

        Args:
            programma_title: str
                Main titel of the whole project
            vacations_title: str
                Titel of the vacations project
            programma_color: str
                First color of the bar
            output_file_name: str
                Base name of the output files
            planning_start: datetime
                Start of the program
            planning_end: datetime
                End of the program
            weeks_margin_left: int
                Shift the end of the planning so many weeks to the left without adding projects
            weeks_margin_right: int
                Shift the end of the planning so many weeks to the right without adding projects
            today: datetime
                Today's date
            dayfirst: bool
                Parse date with the day first
            scale: str
                Which scale is used for the output
            period_info: dict
               Information on the periods output
            excel_info: dict
                Information on the Excel output
            details: bool
                If true, include the details to the programs
            filter_employees: list
                If not None, only add task to which  employees in this list contribute
        """
        self.period_info = period_info
        self.planning_start = planning_start
        self.planning_end = planning_end
        self.date_today = today
        self.dayfirst = dayfirst
        self.scale = scale
        self.details = details
        self.save_svg_as_pdf = save_svg_as_pdf
        self.collaps_tasks = collaps_tasks
        if filter_employees:
            # if filter_employees are given, add them as a set
            self.filter_employees = set(filter_employees)
        else:
            self.filter_employees = None

        self.weeks_margin_left = weeks_margin_left
        self.weeks_margin_right = weeks_margin_right

        self.start_date = planning_start
        self.end_date = planning_end

        if periods is not None:
            for period_key, period_value in period_info.items():
                if period_key in periods:
                    period_start = parse_date(period_value.get("planning_start", self.planning_start))
                    period_end = parse_date(period_value.get("planning_end", self.planning_end))
                    if period_start > self.start_date:
                        self.start_date = period_start
                    if period_end < self.end_date:
                        self.end_date = period_end

        self.excel_info = excel_info

        if output_file_name is None:
            self.output_file_name = Path("gantt_projects.svg")
        else:
            self.output_file_name = Path(output_file_name)

        # Make the main project
        self.programma = gantt.Project(
            name=programma_title, color=color_to_hex(programma_color)
        )

        # Make the project to store all the vacations
        self.vacations_gantt = gantt.Project(
            name=vacations_title, color=color_to_hex(vacation_color)
        )

        self.project_tasks = dict()
        self.vacations = dict()
        self.employees = dict()
        self.tasks_and_milestones = dict()
        self.subprojects = dict()

    @staticmethod
    def add_global_information(
        fill="black", stroke="black", stroke_width=0, font_family="Verdana"
    ):
        gantt.define_font_attributes(
            fill=fill, stroke=stroke, stroke_width=stroke_width, font_family=font_family
        )

    def export_to_excel(self, excel_output_directory):
        """
        Write planning to an Excel file

        Parameters
        ----------
        excel_output_directory: Path
            Output directory of the Excel files
        """

        if self.excel_info is None:
            _logger.warning(
                "Cannot write excel! Please add Excel info to your settings file"
            )
        else:
            excel_output_directory.mkdir(exist_ok=True)
            excel_file = excel_output_directory / self.output_file_name.with_suffix(
                ".xlsx"
            )
            _logger.info(f"Exporting planning to {excel_file}")
            write_planning_to_excel(
                excel_file=excel_file,
                project=self.programma,
                header_info=self.excel_info["header"],
                column_widths=self.excel_info.get("column_widths"),
            )

    def get_dependency(self, key: str) -> gantt.Resource:
        """
        Search the object to which the dependency 'key' refers to

        Parameters
        ----------
        key: str
            Key of the dictionary to which the dependency refers to

        Returns
        -------
        gantt.Resource
            Object to which the  key refers to.
        """

        try:
            depends_of = self.tasks_and_milestones[key]
            if key in self.subprojects.keys():
                _logger.warning(
                    f"The dependency {key} occurs in both tasks en milestones"
                )
            _logger.debug(f"Dependent of task or milestone: {key}")
        except KeyError:
            try:
                depends_of = self.subprojects[key]
                _logger.debug(f"Dependent of project: {key}")
            except KeyError:
                msg = f"Dependency {key} does not exist"
                if self.filter_employees is not None:
                    # in case we are filtering on employees, some dependencies may be missing. Just give a warning
                    _logger.warning(msg)
                    depends_of = None
                else:
                    raise AssertionError(msg)

        return depends_of

    def get_employees(self, employees: Union[str, list]) -> list:
        """
        Turn a list of employees strings into a list of employees gannt.Resource objects

        Parameters
        ----------
        employees: list of str
            List of employees or, in case just one employee is given, a string


        Returns
        -------
        list:
            List of employees resource objects
        """

        employees_elements = list()
        if employees is not None:
            if isinstance(employees, str):
                _logger.debug(f"Adding employee: {employees}")
                employees_elements.append(self.employees[employees].resource)
            else:
                for employee in employees:
                    _logger.debug(f"Adding employee {employee}")
                    employees_elements.append(self.employees[employee].resource)
        return employees_elements

    def get_dependencies(self, dependencies: Union[str, dict]) -> list:
        """
        Retrieve all dependencies

        Parameters
        ----------
        dependencies: str or dict
            In case the dependency is a string, there is only one. This will be obtained from the dict.
            The dependencies may also be stored in a dict. In that case, we retrieve them per item

        Returns
        -------
        list:
            List of dependencies
        """

        dependency_elements = list()

        if dependencies is not None:
            if isinstance(dependencies, str):
                dependent_of = self.get_dependency(dependencies)
                dependency_elements.append(dependent_of)
            elif isinstance(dependencies, dict):
                for category, afhankelijk_items in dependencies.items():
                    for task_key in afhankelijk_items:
                        dependent_of = self.get_dependency(task_key)
                        dependency_elements.append(dependent_of)
            else:
                for afhankelijk_item in dependencies:
                    dependent_of = self.get_dependency(afhankelijk_item)
                    dependency_elements.append(dependent_of)

            return dependency_elements

    def add_vacations(self, vacations_info):
        """
        Add all the vacations
        """
        _logger.info("Adding general holidays")
        for v_key, v_prop in vacations_info.items():
            if v_prop.get("end") is not None:
                _logger.debug(
                    f"Vacation {v_key} from {v_prop['start']} to {v_prop.get('end')}"
                )
            else:
                _logger.debug(f"Vacation {v_key} at {v_prop['start']}")
            self.vacations[v_key] = Vacation(
                start=v_prop["start"], end=v_prop.get("end"), dayfirst=self.dayfirst
            )

    def add_employees(self, employees_info):
        """
        Add the employees with their vacations
        """
        _logger.info("Adding employees...")
        for w_key, w_prop in employees_info.items():
            _logger.debug(f"Adding {w_key} ({w_prop.get('name')})")
            full_name = w_prop.get("name")
            employee_vacations_info = w_prop.get("vacations")
            employee_color = w_prop.get("color")

            self.employees[w_key] = Employee(
                label=w_key,
                full_name=full_name,
                color=employee_color,
                vacations=employee_vacations_info,
            )

            # also add the vacations of this employee to the vacation gantt project in order to give an overview later
            employee_vacations = gantt.Project(
                name=full_name,
                color=employee_color,
                font=gantt.get_font_attributes(font_weight="bold", font_size="20"),
            )
            if employee_vacations_info is not None:
                for v_key, v_prop in employee_vacations_info.items():
                    vacation_name = v_prop.get("label", v_key)
                    vacation_start = v_prop.get("start")
                    vacation_end = v_prop.get("end")
                    if vacation_end is None:
                        vacation_duration = 1
                    else:
                        vacation_duration = None
                    vacation_task = Task(
                        label=vacation_name,
                        color=v_prop.get("color"),
                        start=vacation_start,
                        end=vacation_end,
                        duration=vacation_duration,
                        dayfirst=self.dayfirst,
                    )
                    employee_vacations.add_task(vacation_task.element)
            self.vacations_gantt.add_task(employee_vacations)

    def make_task_of_milestone(
        self,
        task_properties: dict = None,
        project_color=None,
    ) -> Union[Task, Milestone]:
        """
        Add all the general tasks and milestones

        Parameters
        ----------
        task_properties: dict
            Dictionary with tasks or milestones
        project_color: str
            Color of the parent project

        Returns
        -------
        Task or milestone

        """
        dependencies = self.get_dependencies(task_properties.get("dependent_of"))
        element_type = task_properties.get("type", "task")
        if element_type == "task":
            employees = self.get_employees(task_properties.get("employees"))
            _logger.debug(f"Voeg task {task_properties.get('label')} toe")
            task_or_milestone = Task(
                label=task_properties.get("label"),
                start=task_properties.get("start"),
                end=task_properties.get("end"),
                duration=task_properties.get("duration"),
                color=task_properties.get("color"),
                project_color=project_color,
                detail=task_properties.get("detail", False),
                employees=employees,
                dependent_of=dependencies,
                dayfirst=self.dayfirst,
            )
        elif element_type == "milestone":
            _logger.debug(f"Adding milestone {task_properties.get('label')} toe")
            if task_properties.get("end"):
                raise ValueError(
                    "You have specified a milestone, but also defined an end date. Milestones only"
                    f"require a start data. Please fix task\n{task_properties}"
                )
            task_or_milestone = Milestone(
                label=task_properties.get("label"),
                start=task_properties.get("start"),
                color=task_properties.get("color"),
                project_color=project_color,
                dependent_of=dependencies,
                dayfirst=self.dayfirst,
            )
        else:
            raise AssertionError("Type should be 'task' or 'milestone'")

        # add all the remain fields which are not required for the gantt charts but needed for the Excel output
        for task_key, task_value in task_properties.items():
            if not hasattr(task_or_milestone.element, task_key):
                if isinstance(task_value, str):
                    try:
                        _task_value = parse_date(
                            task_value, task_value, dayfirst=self.dayfirst
                        )
                    except ParserError:
                        _logger.debug(f"task {task_key} is not an date. No problem")
                    else:
                        _logger.debug(
                            f"Converted string {task_value} into datetime {_task_value}"
                        )
                        task_value = _task_value
                _logger.debug(f"Adding task {task_key} with value {task_value}")
                setattr(task_or_milestone.element, task_key, task_value)

        return task_or_milestone

    def add_tasks_and_milestones(
        self, tasks_and_milestones=None, tasks_and_milestones_info=None
    ):
        """
        Make all tasks en milestones
        """

        _logger.info("Voeg alle algemene tasks en mijlpalen toe")
        if tasks_and_milestones_info is not None:
            # The tasks are organised in modules, to peel of the first level
            tasks_en_mp = dict()
            for module_key, module_values in tasks_and_milestones_info.items():
                _logger.debug(f"Reading tasks of module {module_key}")
                for task_key, task_val in module_values.items():
                    _logger.debug(f"Processing task {task_key}")
                    if task_key in tasks_en_mp.keys():
                        msg = f"De task key {task_key} has been used before. Please pick another name"
                        _logger.warning(msg)
                        raise ValueError(msg)
                    if self.filter_employees is not None:
                        contributors = task_val.get("employees")
                        is_contributing = check_if_employee_in_contributing(
                            filter_employees=self.filter_employees,
                            contributing_employees=contributors,
                        )
                        if not is_contributing:
                            _logger.debug(
                                f"None of {contributors} are in {self.filter_employees}. Skipping"
                            )
                            continue
                    tasks_en_mp[task_key] = tasks_and_milestones_info[module_key][
                        task_key
                    ]
        else:
            tasks_en_mp = tasks_and_milestones

        for task_key, task_val in tasks_en_mp.items():
            _logger.debug(f"Processing task {task_key}")
            self.tasks_and_milestones[task_key] = self.make_task_of_milestone(
                task_properties=task_val
            )

    def make_projects(
        self,
        subprojects_info,
        subprojects_title,
        subprojects_selection,
        subprojects_color=None,
    ):
        """
        Make all projects
        """
        employee_color = color_to_hex(subprojects_color)

        projects_employee = gantt.Project(
            name=subprojects_title,
            color=employee_color,
            font=gantt.get_font_attributes(font_weight="bold", font_size="20"),
        )

        added_projects = list()

        _logger.info(f"Add all projects of {subprojects_title}")
        for project_key, project_values in subprojects_info.items():
            project_name = project_values.get("title", project_key)
            project_name_collapsed = project_values.get("title_collapsed", project_name)
            projects_employee_collapsed = project_values.get("employees_collapsed")
            if projects_employee_collapsed is not None and isinstance(
                projects_employee_collapsed, str
            ):
                projects_employee_collapsed = [projects_employee_collapsed]

            _logger.info(f"Making project: {project_name}")

            project_color = color_to_hex(project_values.get("color"))

            _logger.debug("Creating project {}".format(project_name))
            project = gantt.Project(name=project_name, color=project_color)

            main_start_date = None
            main_end_date = None
            main_contributors = None

            # add all the other elements as attributes
            for p_key, p_value in project_values.items():
                if not hasattr(project, p_key):
                    setattr(project, p_key, p_value)

            if project_key in self.subprojects.keys():
                msg = f"project {project_key} already exists. Pick another name"
                _logger.warning(msg)
                raise ValueError(msg)

            self.subprojects[project_key] = project

            if tasks := project_values.get("tasks"):
                if isinstance(tasks, list):
                    tasks_dict = {k: k for k in tasks}
                else:
                    tasks_dict = tasks

                for task_key, task_val in tasks_dict.items():
                    if isinstance(task_val, dict):
                        is_detail = task_val.get("detail", False)
                    else:
                        is_detail = False
                    if not self.details and is_detail:
                        # We hebben details op False staan en dit is een detail, dus sla deze task over.
                        _logger.info(
                            f"Skipping task {task_key} because it is set to be a detail"
                        )
                        continue

                    _logger.debug("Adding task {}".format(task_key))

                    is_detail = False

                    if isinstance(task_val, str):
                        try:
                            # de task een task of een milestone?
                            task_obj = self.tasks_and_milestones[task_val]
                            task = task_obj.element
                            is_detail = task_obj.detail
                        except KeyError:
                            try:
                                # de task een ander project?
                                task = self.subprojects[task_val]
                            except KeyError as err:
                                if not self.filter_employees:
                                    _logger.warning(f"{err}")
                                    raise
                                else:
                                    _logger.debug(f"{err}")
                                    continue
                    else:
                        task_obj = self.make_task_of_milestone(
                            task_properties=task_val, project_color=project_color
                        )
                        task = task_obj.element
                        is_detail = task_obj.detail

                    if task.color is None:
                        task.color = project_color

                    if self.filter_employees:
                        try:
                            contributors = task.employees
                        except AttributeError:
                            if isinstance(task, gantt.Task):
                                _logger.debug(
                                    "No employees found and this is a task. Skip it!"
                                )
                                continue
                            else:
                                _logger.debug(
                                    "No employees found, but can be a projects, so just add"
                                )
                        else:
                            is_contributing = check_if_employee_in_contributing(
                                filter_employees=self.filter_employees,
                                contributing_employees=contributors,
                            )
                            if not is_contributing:
                                _logger.debug(
                                    f"None of {contributors} are in {self.filter_employees}. Skipping"
                                )
                                continue

                    if not self.details and is_detail:
                        _logger.debug(f"skipping task {task_key} as it is a detail")
                    else:
                        if not self.collaps_tasks or isinstance(task, gantt.Project):
                            added_projects.append(project_key)
                            project.add_task(task)

                        if projects_employee_collapsed is None:
                            main_contributors = get_contributors_task(
                                task,
                                main_contributors,
                            )
                        else:
                            main_contributors = get_contributors_from_resources(
                                projects_employee_collapsed,
                                main_contributors,
                                self.employees,
                            )

                        # each project with task is stored as a main project with the project begin and end
                        if (
                            main_start_date is None
                            and self.start_date <= task.start_date() < self.end_date
                        ):
                            main_start_date = task.start_date()
                        try:
                            task_end_date = task.end_date()
                        except AssertionError:
                            main_end_date = None
                        else:
                            main_end_date = min(self.end_date, task_end_date)
                        if (
                            main_start_date is not None
                            and self.start_date < task.start_date() < main_start_date
                        ):
                            main_start_date = task.start_date()

                        if (
                            main_end_date is not None
                            and main_end_date < task.end_date() <= self.end_date
                        ):
                            main_end_date = task.end_date()

            # every project with tasks will be a course project plan as well
            if (
                self.collaps_tasks
                and main_start_date is not None
                and project_key not in added_projects
            ):
                if main_contributors is not None:
                    main_contributors = list(set(main_contributors))
                if main_end_date is None:
                    main_task = gantt.Task(
                        name=project_name_collapsed,
                        start=main_start_date,
                        duration=1,
                        resources=main_contributors,
                    )
                else:
                    main_task = gantt.Task(
                        name=project_name_collapsed,
                        start=main_start_date,
                        stop=main_end_date,
                        resources=main_contributors,
                    )
                if project is not None:
                    project.add_task(main_task)

            self.subprojects[project_key] = project
            if project_key in subprojects_selection:
                # hier project zonder taken toevoegen
                projects_employee.add_task(project)

        # add now all projects of the employee to the program
        self.programma.add_task(projects_employee)

    def write_planning(
        self,
        planning_output_directory,
        resource_output_directory,
        vacations_output_directory,
        write_resources=False,
        write_vacations=False,
        periods=None,
    ):
        """
        Write the planning to the output definitions

        Parameters
        ----------
        write_resources: bool
            Write the resources file as well (next to the gantt charts which is always written)
        write_vacations: bool
            Write the vacations file as well
        planning_output_directory: Path
            Output directory of the svg files of the planning
        resource_output_directory: Path
            Output directory of the svg files of the resources
        vacations_output_directory: Path
            Output directory of the svg files of the vacations
        periods: list
           Periods we want to add. If None, add all periods
        """

        directories = {
            "tasks": planning_output_directory,
            "resources": resource_output_directory,
            "vacations": vacations_output_directory,
        }
        svg42pdf = None
        # make output directories. Vacations can be made per period, so do later
        directories["tasks"].mkdir(parents=True, exist_ok=True)
        if write_resources:
            directories["resources"].mkdir(parents=True, exist_ok=True)

        for period_key, period_prop in self.period_info.items():
            if periods is not None and period_key not in periods:
                _logger.debug(f"Employee {period_key} is skipped")
                continue

            file_names = dict()
            leading_suffix = [period_key]
            if self.collaps_tasks:
                leading_suffix += ["collapsed"]

            write_vacations_this_period = period_prop.get("export_vacations", False)

            for file_suffix in directories.keys():
                file_names[file_suffix] = extend_suffix(
                    self.output_file_name, extensions=leading_suffix + [file_suffix]
                )
                file_names[file_suffix] = (
                    directories[file_suffix] / file_names[file_suffix]
                )

            weeks_margin_left = period_prop.get(
                "weeks_margin_left", self.weeks_margin_left
            )
            weeks_margin_right = period_prop.get(
                "weeks_margin_right", self.weeks_margin_right
            )

            scale = period_prop.get("scale")
            if scale is not None:
                scale = SCALES[scale]
            else:
                scale = self.scale

            start = parse_date(
                period_prop.get("planning_start"),
                self.planning_start,
                dayfirst=self.dayfirst,
            )
            end = parse_date(
                period_prop.get("planning_end"),
                self.planning_end,
                dayfirst=self.dayfirst,
            )

            today = parse_date(
                period_prop.get("today"), self.date_today, dayfirst=self.dayfirst
            )
            if today is not None and scale != SCALES["daily"]:
                # For any scale other than  daily, the today-line is drawn only at Saturdays
                _logger.debug("Change the date to the nearest Saturday")
                _today = today
                today = get_nearest_saturday(today)
                if today != _today:
                    _logger.debug(
                        f"Changing the date today {_today} into the the nearest Saturday {today}"
                    )

            # the planning is a collection of all the projects
            file_name = file_names["tasks"]
            _logger.info(
                f"Writing project starting at {start} and ending at {end} with a scale {scale} to {file_name}"
            )
            self.programma.make_svg_for_tasks(
                filename=file_name,
                start=start,
                end=end,
                margin_left=weeks_margin_left,
                margin_right=weeks_margin_right,
                scale=scale,
                today=today,
            )

            if self.save_svg_as_pdf:
                try:
                    import svg42pdf
                except ImportError as err:
                    _logger.warning(f"{err}\nFailed writing pdf because svg42pdf is")
                else:
                    pdf_file_name = file_name.with_suffix(".pdf")
                    _logger.info(f"Saving as {pdf_file_name}")
                    svg42pdf.svg42pdf(
                        svg_fn=file_name.as_posix(),
                        pdf_fn=pdf_file_name.as_posix(),
                        method="any",
                    )

            if write_resources:
                file_name_resources = file_names["resources"]
                _logger.info(
                    f"Write resources of {start} to {end} with scale {scale} to {file_name_resources}"
                )
                try:
                    self.programma.make_svg_for_resources(
                        filename=file_name_resources.as_posix(),
                        start=start,
                        end=end,
                        scale=SCALES["daily"],
                        today=today,
                    )
                except TypeError as err:
                    _logger.warning(err)
                    _logger.warning(
                        "Failed writing the resources with the above error message. Please check your "
                        "employee's input data"
                    )
                else:
                    if self.save_svg_as_pdf and svg42pdf is not None:
                        pdf_file_name_res = file_name_resources.with_suffix(".pdf")
                        svg42pdf.svg42pdf(
                            svg_fn=file_name_resources.as_posix(),
                            pdf_fn=pdf_file_name_res.as_posix(),
                            method="any",
                        )

            if write_vacations or write_vacations_this_period:
                file_name_vacations = file_names["vacations"]
                vacations_output_directory.mkdir(exist_ok=True, parents=True)
                _logger.info(f"Writing vacation file {file_name_vacations}")
                self.vacations_gantt.make_svg_for_tasks(
                    filename=file_name_vacations,
                    start=start,
                    end=end,
                    margin_left=weeks_margin_left,
                    margin_right=weeks_margin_right,
                    scale=scale,
                    today=today,
                )
                if self.save_svg_as_pdf and svg42pdf is not None:
                    pdf_file_name_vac = file_name_vacations.with_suffix(".pdf")
                    svg42pdf.svg42pdf(
                        svg_fn=file_name_vacations.as_posix(),
                        pdf_fn=pdf_file_name_vac.as_posix(),
                        method="any",
                    )

            _logger.debug("Done")


def check_if_employee_in_contributing(
    filter_employees: list, contributing_employees: list
) -> bool:
    """
    Check if any of the employees given in filter_employees is in contributing to this taks
    """

    is_contributing = False

    if contributing_employees:
        if isinstance(contributing_employees, str):
            contributing_employees = set(list([contributing_employees]))
        else:
            contributing_employees = set(contributing_employees)
        if contributing_employees.intersection(filter_employees):
            _logger.debug(
                f"Contributing employees {contributing_employees} not in filter list"
            )
            is_contributing = True

    return is_contributing


def extend_suffix(output_filename: Path, extensions: Union[list, str]):
    """
    Add an extra suffix to the base filename

    Parameters
    ----------
    output_filename: Path
        Base filename
    extensions: str or list
        Extra suffixes to add

    Returns
    -------
    Path:
        New filename with extra suffix

    """
    suffix = output_filename.suffix
    if isinstance(extensions, str):
        extensions = [extensions]
    output_filename = Path(
        "_".join([output_filename.with_suffix("").as_posix()] + extensions)
    ).with_suffix(suffix)

    return output_filename


def get_contributors_task(task, contributors):
    """
    get of the contributors of this Task based on the task resources

    Parameters
    ----------
    task
    contributors

    Returns
    -------
    list:
        contributors

    """
    try:
        task_resources = task.resources
    except AttributeError:
        pass
    else:
        if task_resources:
            for employee in task_resources:
                if contributors is None:
                    contributors = [employee]
                else:
                    contributors.append(employee)
    return contributors


def get_contributors_from_resources(
    projects_employee_global, contributors, all_resources
):
    """
    get the contributors of this Task based on the global resources

    Parameters
    ----------
    projects_employee_global
    contributors
    all_resources: list

    Returns
    -------
    list:
        contributors

    """
    for emp_key, emp_val in all_resources.items():
        if emp_key in projects_employee_global:
            if contributors is None:
                contributors = [emp_val.resource]
            else:
                contributors.append(emp_val.resource)
    return contributors
