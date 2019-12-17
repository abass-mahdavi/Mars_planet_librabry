SECURITY_SETTINGS = dict(
    APP_SECRET_KEY="deleted"",  # mpt_pub_arg_secret_b10
    GOODREADS_KEY="deleted", # deleted for security reasons to get it : mpt_pub arg R3 message: 㙱㟂㚽㠲㑊㠷㪹㖚㬜㕏㥌㑽㝣㧇㤳㜞㖲ㇾ㚪㝈㜿㧩㡠㐄㙾㭡㛿㨸㫰㯗㮽㓺㘓㞚㛿㓲㚼㙡㟝㥙㦝㫋㝪㯏㑀㨋㫰㚄㦸㭚㗀㯦㮌㭞㑎㣍㨬㦍㗬㡉㣉㕕㞦㡝㫧㐅㨵㞤㒤㬀㝟㮰㝖㤎㑙㨪㪕㩜㟕㞉㕓㠝㬹㕪㢉㪅㟬㚫㡈㢌㩽㭸㕠㥈㪑㞒㨖㠀㑕㢓㨈㚈㥁㦽㞩㫼㘣㛯㚶㦬㭭㑡㬗㫲㪊㤕㥤㥱㔪㐧㥾
    DATABASE_URL="postgresql://me:pw@localhost:5432/cs_50_books", #URL of the database, it depends on the database configuration  deleted for security reasons
    DEBUG_MODE="True", # should be False on production
)

COLORS = dict(
    LOGO="#00ff99",
    COURTESY_MESSAGE="#555555",
    NAV_LINKS="#3385ff",
    BODY_BACKGROUND="#000000",
    BODY_FONT="#ffffff",
    USER_LOGGED="#ffff000",
    LOGOUT = "ff00000",
)

SETTINGS = dict(
    CONSTANTS=dict(
        BODY_BACKGROUND_COLOR=COLORS.get("BODY_BACKGROUND"),
        BODY_FONT_COLOR=COLORS.get("BODY_FONT"),
        PROJECT_LOGO="* * * Mars * Planet * Library * * *",
        LOGO_COLOR=COLORS.get("LOGO"),
        NAV_BAR_LINKS_COLOR=COLORS.get("NAV_LINKS"),
        NAV_BAR_LINKS_COLOR_USER_LOGGED=COLORS.get("USER_LOGGED"),
        NAV_BAR_LINKS_LOGOUT=COLORS.get("LOGOUT"),
        COURTESY_IMAGE_COLOR=COLORS.get("COURTESY_MESSAGE"),
        # pages titles
        HOME_PAGE_TITLE="MPL-Home",
        REGISTRATION_PAGE_TITLE="MPL-Register",
        LOGIN_PAGE_TITLE="MPL-Login",
        ABOUT_PAGE_TITLE="MPL-About",
        SEARCH_PAGE_TITLE="MPL-Search",
        SEARCH_RESULTS_PAGE_TITLE="MPL-Results",
        IMPORT_BOOK_PAGE = "MPL-Import",
        BOOK_PAGE="MPL-Book",
        # pages names
        HOME_PAGE="Home",
        ABOUT_PAGE="About",
        LOGIN_PAGE="Login",
        LOGOUT_PAGE="Logout",
        SEARCH_PAGE="Search",
        REGISTRATION_PAGE="Register",
        HOME_WELCOME_MESSAGE="""
            <center>               
                <img src="https://mars.nasa.gov/system/resources/detail_files/3550_3550_PIA14293-amended1.jpg" alt="mars" width=50%>
                <br><h7><font color={}>Image Courtesy: NASA</font></h7><br><br>
                <h4>Welcome to: </h4>
                <h4><font color={}>* * * Mars * Planet * Library * * * </font></h4>
            </center> """.format(
            COLORS.get("COURTESY_MESSAGE"), COLORS.get("LOGO")
        ),
        # About page and route
        ABOUT_PAGE_MESSAGE="""<div style="padding-left: 10% ; padding-right: 10%">
            <h4>
                <font color={}>* * * Mars * Planet * Library * * * </font>
            is an online readers community (well, sort of). </h4>
            <h4> Once you have regitered an account (it is easy), you'll be able to: </h4>
            <ul>
                <li>search books available in our catalog</li>
                <li>view the book details</li>
                <li>veiw the ratings and feedbacks left by others memebers</li>
                <li>rate any book and write a review about it</li>
            </ul>
            <h4>Please click "login" button to login your account or click "register" to become a member</h4>
            <h4>...and in case you have already looged in click "search" to get access to our book catalog</h4></div>""".format(
            COLORS.get("LOGO")
        ),
        # registration page and route
        REGISTRATION_WELCOME_MESSAGE="<i><h4>Register now and </h4><h4>get access to </h4><h4>**Mars*Planet*Library**</h4><h4>members pages:</h4></i>",
        
        FLASH_MESSAGE_ACCOUNT_CREATED_FOR="Account created for",
        ALREAY_HAVE_AN_ACCOUNT="Already Have An Account?",
        IS_ALREADY_REGISTERED="is already registered, please try a different username",
        REGISTRATION_FAILED=" oups, registration failed, please try again later or contact the webiste administrator",
        SIGN_IN="Sign In",
        # login page and route
        LOGIN_WELCOME_MESSAGE="<i><h4>Login here to access</h4><h4>**Mars*Planet*Library**</h4><h4>members pages:</h4></i>",
        FLASH_MESSAGE_SUCCESSFUL_LOGIN="You have been logged in!",
        FLASH_MESSAGE_LOGIN_FAILURE="Login Unsuccessful. Please check username and password",
        NEED_AN_ACCOUNT="Need An Account? ",
        REGISTER_NOW="Register now",
        FORGOT_PASSWORD="Forgot Password?",
        LOGGED_USER_GREETING="hello ",
        # database_requests
        USERNAME_ALREADY_REGISTERED="is already registered",
        # search
        ONE_FIELD_AT_LEAST_REQUIRED = "Please complete at least one field",
        SEARCH_WELCOME_MESSAGE="Please complete at least one field and click search button",
        AUTHOR="Author",
        TITLE="Title",
        ISBN="ISBN",
        PUBLICATION_YEAR = "Publication year",
        DETAILS="More details",
        # book and reviews
        FLASH_MESSAGE_SUCCESSFUL_REVIEW = "Your review was successfully submited",
        FLASH_MESSAGE_REVIEW_FAILURE = "Oupss something went wrong, your review could nor be submitted, pleae contact the webmaster",
        FEATURED_BOOK = "Featured book:",
        NUMBER_OF_MPL_REVIEWS="MPL(*) total reviews ",
        AVERAGE_MPL_RATING="MPL(*) average review rating ",
        GOODREADS_REVIEWS_COUNT = "Goodreads total reviews ",
        GOODREADS_AVERAGE_REVIEW_SCORE="Goodreads average rating ",
        MPL_STANDS_FOR_MARS_PLANET_LIBRARY="(*) MPL stands for ***Mars*Planet*Library***",
        BOOK_ALREADY_REVIEWED_MESSAGE="You have already reviewed and rated the featured book",
        BE_THE_FIRST_TO_REVIEW_MESSAGE = "Be the first to rate and review the featured book:",
        RATE_AND_REVIEW_MESSAGE = "please rate and review the featured book:",
        PLEASE_SELECT_A_RATING_1_5 = "Please select a rating for the featured book (1-5)",
        BOOK_REVIEWS = "Featured book reviews:",
        REVIEWER_USERNAME="reviewer username",
        RATING = "rating",
        REVIEW = "review",
        NOT_RELEVANT = "Not relevant",
        BOOK_DATAS = "book_details",
        GOODREADS_DATAS = "goodreads_datas",
        REVIEWS = "reviews",
        NUMBER_OF_REVIEWS = "number_of_reviews",
        AVERAGE_REVIEW_SCORE = "average_review_score",

        # import
        IMPORT_CSV_BOOK_CATALOG_FILE = "IMPORT CSV BOOK CATALOG FILE"

    ),
    API_FIELDS = dict(
        TITLE = "title",
        AUTHOR= "author",
        YEAR = "year", 
        REVIEW_COUNT = "review_count",
        AVERAGE_COUNT = "average_score",

    ),
    FORMS=dict(
        USERNAME="Username",
        EMAIL="Email",
        PASSWORD="Password",
        CONFIRM_PASSWORD="Confirm Password",
        SIGN_UP="Sign Up",
        FORM_CONTROL="form-control form-control-sm bg-dark text-white",
        FORM_CONTROL_INVALID="form-control form-control-sm bg-dark text-white is-invalid",
        REMMEMBER_ME="Remember Me",
        LOGIN="Login",
        ISBN="ISBN",
        AUTHOR_NAME="Author name",
        BOOK_TITLE="Book Title",
        SEARCH="Search",
        REVIEW_INVITE = "Please write a review and click submit button:",
        SUBMIT_REVIEW = "submit review",
        IMPORT_BOOKS = "import new csv book catalog",
        IMPORT_CSV_FILE = "upload cvs file",
    ),
)

#fuctions
def book_search_result_message(number_of_books):
    if number_of_books == 0:
        return "your search produced no result:"
    elif number_of_books == 1:
        return "your search produced one result:"
    else:
        return "your search produced " + str(number_of_books) + " results:"
