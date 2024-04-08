from diagrams import Diagram, Cluster, Edge
from diagrams.programming.flowchart import Action, InputOutput, Decision
from diagrams.onprem.network import Internet

with Diagram("Hospital Price Transparency File Download Workflow", show=False, direction="LR"):  # Changed direction to Left to Right
#     with Cluster("Initialization"):
#         suppress_warnings = Action("Suppress HTTPS Warnings ")
#         define_states_zip_codes = InputOutput("Define States & ZIP Codes ")
#         setup_directories = Action("Setup Base Directory ")
#         initialize_session = Action("Initialize HTTP Session ")
#         progress_bar_setup = Action("Setup Progress Bar ")
#         load_progress_file = Decision("Load Progress File ")

    # with Cluster("Main Download Loop"):
    #     construct_url = Action("Construct Search URL ")
    #     fetch_data = Internet("Fetch Facility Data ")
    #     prepare_download_path = Action("Prepare Download Path ")
    #     download_file = Action("Download File ")
    #     update_progress = Action("Update Progress Bar & Log ")
    #
    with Cluster("Finalization"):
        close_progress_bar = Action("Close Progress Bar ")
        log_final_progress = InputOutput("Log Final Progress ")
    #
    # with Cluster("Collection Failure"):
    #     failed_downloads = Decision("If Download Failed ")

    # Define connections by stacking each group of actions on top of each other
    # Initialization group first
    #suppress_warnings >> define_states_zip_codes >> setup_directories >> initialize_session >> progress_bar_setup >> load_progress_file
    # # Main download loop group
        #construct_url >> fetch_data >> prepare_download_path >> download_file >> update_progress
    # # Finalization group
        log_final_progress >> close_progress_bar
    # # Connect the groups
    # close_progress_bar << Edge(color="black") << progress_bar_setup
