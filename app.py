import plotly.express as px
import seaborn as sns
from shiny.express import input, ui
from shiny import render  # Import render module
from shinywidgets import render_plotly
import palmerpenguins  # provides the Palmer Penguin dataset

# Use the built-in function to load the Palmer Penguins dataset
penguins_df = palmerpenguins.load_penguins()

ui.page_opts(title="Mrs. Doodles Penguins", fillable=True)

# Add a Shiny UI sidebar for user interaction
with ui.sidebar(open="open"):

    # Use the ui.h2() function to add a 2nd level header to the sidebar
    # pass in a string argument (in quotes) to set the header text to "Sidebar"
    ui.h2("Sidebar")

    # Use ui.input_selectize() to create a dropdown input to choose a column
    ui.input_selectize("selected_attribute", "Selected Attribute",
                       ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"])

    # Use ui.input_numeric() to create a numeric input for the number of Plotly histogram bins
    ui.input_numeric("plotly_bin_count", "Plotly Bin Count", 40)

    # Use ui.input_slider() to create a slider input for the number of Seaborn bins
    ui.input_slider("seaborn_bin_count", "Seaborn Bin Count", 0, 100, 40)

    # Use ui.input_checkbox_group() to create a checkbox group input to filter the species
    ui.input_checkbox_group("selected_species_list", "Species",
                            ["Adelie", "Gentoo", "Chinstrap"], selected=["Adelie","Gentoo", "Chinstrap"])

    # Use ui.input_checkbox() to create a checkbox to show the sex
    ui.input_checkbox("show_sex", "Show Sex")

    # Use ui.hr() to add a horizontal rule to the sidebar
    ui.hr()

    # Use ui.a() to add a hyperlink to the sidebar
    ui.a("GitHub", href="https://github.com/Ldooley32/cintel-02-data-doodles/tree/main", target="_blank")

with ui.layout_columns():
    with ui.accordion(id="acc", open="open"):
        with ui.accordion_panel("Data Table"):
            @render.data_frame
            def penguin_datatable():
                return render.DataTable(penguins_df)

        with ui.accordion_panel("Data Grid"):
            @render.data_frame
            def penguin_datagrid():
                return render.DataGrid(penguins_df)

with ui.navset_card_tab(id="tab"):
    with ui.nav_panel("Plotly Histogram"):

        # Create a function to render the Plotly histogram
        @render_plotly
        def plotly_histogram():
            # Create a Plotly histogram with dynamic attributes and bin count based on user inputs
            selected_attribute = input.selected_attribute()
            plotly_bin_count = input.plotly_bin_count()
            selected_species_list = input.selected_species_list()
            show_sex = input.show_sex()

            filtered_df = penguins_df[penguins_df["species"].isin(selected_species_list)]

            if show_sex:
                title = f"Plotly Histogram for {selected_attribute} (Sex Included)"
                xaxis_title = f"{selected_attribute} (with Sex)"
            else:
                title = f"Plotly Histogram for {selected_attribute}"
                xaxis_title = selected_attribute

            histogram = px.histogram(
                filtered_df,
                x=selected_attribute,
                color="sex" if show_sex else None,
                title=title,
                labels={selected_attribute: xaxis_title},
                nbins=plotly_bin_count,
            )
            return histogram

    with ui.nav_panel("Seaborn Histogram"):
            # Create a function to render the Seaborn histogram
            @render.plot
            def seaborn_histogram():
                    selected_attribute = input.selected_attribute()
                    seaborn_bin_count = input.seaborn_bin_count()
                    show_sex = input.show_sex()
                    selected_species_list = input.selected_species_list()

                    filtered_df = penguins_df[penguins_df["species"].isin(selected_species_list)]

                    title = f"Seaborn Histogram for {selected_attribute}"
                    if show_sex:
                        title += " (Sex Included)"

                    sns.set(style="whitegrid")  # Set Seaborn style
                    seaborn_histogram = sns.histplot(
                        filtered_df,
                        x=selected_attribute,
                        hue="sex" if show_sex else None,
                        bins=seaborn_bin_count,
                    )
                     # Update titles and labels
                    seaborn_histogram.set_title(title)
                    
                    return seaborn_histogram
                
    with ui.nav_panel("Scatterplot"):
        ui.card_header("Plotly Scatterplot: Species")
                 
        @render_plotly
        def ploty_scatterplot():
            selected_species_list = input.selected_species_list()
            filtered_df = penguins_df[penguins_df["species"].isin(selected_species_list)]
            plotly_scatter = px.scatter(
                filtered_df,
                x="body_mass_g",
                y="bill_length_mm",
                color="species",
                size_max=7,
                labels={
                    "body_mass_g": "Body Mass (g)",
                    "bill_length_mm": "Bill Length(mm)",
                },
            )
            return plotly_scatter
