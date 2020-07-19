import bs4
import requests
from bs4 import BeautifulSoup


class RottenTomatoesScraper:
    def __init__(self, source: str):
        """Scrape movie reviews from Rotten Tomatoes.

        Args:
            source (str): URL of movie's page on RT.
        """
        src_content = self.fetch_src_content(source)
        soup = BeautifulSoup(src_content, "lxml")
        self.review_scores: list = self.extract_review_scores(soup)
        self.review_text: list = self.extract_review_text(soup)
        self.title: str = self.extract_movie_title(soup)

    def to_dict(self):
        """Return Pandas-compatible dictionary of reviews.
        """
        title = [self.title for review in self.review_scores]
        return {
            "Title": title,
            "Review Text": self.review_text,
            "Scores": self.review_scores,
        }

    def fetch_src_content(self, source: str) -> bytes:
        """Fetch page bytecontent from source URL.

        Args:
            source (str): source URL.
        
        Raises:
            StatusError: Raises respective error for non-200 responses.

        Returns:
            bytes: bytecontent of page.
        """
        src = requests.get(source)
        src.raise_for_status()
        return src.content

    def extract_movie_title(self, soup: BeautifulSoup) -> str:
        """Extract movie title text from given soup.

        Args:
            soup (BeautifulSoup): Soup of source page.

        Raises:
            NotFoundError: Raised if movie title is not found.

        Returns:
            str: Title of movie.
        """
        title_dirty: str = soup.find("h2", class_="panel-heading").text
        if not title_dirty:
            raise NotFoundError("movie title")
        # Fake Movie Title R̶e̶v̶i̶e̶w̶s̶
        title = title_dirty[:-8]
        return title

    def extract_review_text(self, soup: BeautifulSoup) -> list:
        """Extract text from reviews on given soup.

        Args:
            soup (BeautifulSoup): Soup of source page.

        Raises:
            NotFoundError: Raised if no review texts are found.

        Returns:
            list: List of text from reviews.
        """
        reviews = soup.find_all("p", class_="audience-reviews__review")

        if not reviews:
            raise NotFoundError("review text")

        review_text = [review.text for review in reviews]
        return review_text

    def extract_review_scores(self, soup: BeautifulSoup) -> list:
        """Extract scores out of 5 from reviews on given soup.

        Args:
            soup (BeautifulSoup): Soup of source page.

        Raises:
            NotFoundError: Raised if no star-display HTML tags are found.

        Returns:
            list: List of scores
        """
        # star-display is the HTML class RT uses for the stars
        star_displays = soup.find_all(class_="star-display")

        if not star_displays:
            raise NotFoundError("star-display tags")

        review_scores = [
            self.calculate_score(star_display) for star_display in star_displays
        ]
        return review_scores

    def calculate_score(self, star_display: bs4.element.Tag) -> int:
        """Calculate numerical score from number of star-display elements.

        Args:
            star_display (bs4.element.Tag): RT website class for star-display's

        Raises:
            TypeError: Raised if input is not of type bs4.element.Tag
            TypeError: Raised if tag is not of class 'star-display'

        Returns:
            int: Numerical score.
        """
        if not isinstance(star_display, bs4.element.Tag):
            raise TypeError("Input must be of type bs4.element.Tag")
        if not star_display["class"][0] == "star-display":
            raise TypeError("Tag must be of class 'star-display'")

        full_star_count = len(
            star_display.find_all(class_="star-display__filled", recursive=False)
        )
        half_star_count = len(
            star_display.find_all(class_="star-display__half", recursive=False)
        )  # NOTE: Not too sure if BS4 has inbuilt function for this

        score = full_star_count + (half_star_count * 0.5)
        return score


class NotFoundError(Exception):
    def __init__(self, missing: str = "reviews", *args, **kwargs):
        """No {missing} was/were found in page.
        """
        self.missing = missing
        super().__init__(*args, **kwargs)

    def __str__(self):
        return f"No {self.missing} was/were found in page."
