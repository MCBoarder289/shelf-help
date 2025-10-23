import os

from openai import OpenAI
from shelfhelp_api.models import BookRecommendations, BookRecommendation

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

reference_books_ex = "The Sparrow by Mary Doria Russell, Station Eleven by Emily St. John Mandel, The Left Hand of Darkness by Ursula K. Le Guin"


def get_recommendations(reference_books: str) -> BookRecommendations:

    prompt = f"""
    Given the following reference books: {reference_books}
    
    Find 3-5 similar or thematically related books that a reader might also enjoy. 
    For each, return the exact direct Goodreads URL to the book's page (not list or author pages).
    
    Respond in the following JSON format:
    {{ "recommendations": [{{ "link": "..." }}] }}
    """


    response = client.responses.parse(
        model="gpt-5-nano",
        tools=[{"type": "web_search"}],
        input=prompt,
        text_format=BookRecommendations,
    )

    return response.output_parsed

def get_recommendations_mock(reference_books: str) -> BookRecommendations:
    print(reference_books)
    return BookRecommendations(
        recommendations=[
            BookRecommendation(link='https://www.goodreads.com/book/show/11955654-embassytown'),
            BookRecommendation(link='https://www.goodreads.com/book/show/95558.Solaris'),
            BookRecommendation(link='https://www.goodreads.com/book/show/25563522-children-of-time'),
            BookRecommendation(link='https://www.goodreads.com/book/show/894464.The_Dispossessed'),
            BookRecommendation(link='https://www.goodreads.com/book/show/6288.The_Road')
        ]
    )


if __name__ == "__main__":
    get_recommendations_mock(reference_books=reference_books_ex)