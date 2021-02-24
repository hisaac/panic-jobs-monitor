import json
import requests
from bs4 import BeautifulSoup

def lambda_handler(event, context):

    try:
        html = requests.get("https://panic.com/jobs/")
    except requests.RequestException as error:
        print(error)
        raise error

    soup = BeautifulSoup(html.text, 'html.parser')
    current_openings = soup.select('.openings')[0]

    expected_html = """
            <section class="openings">
                <div class="content">
                    <h2>Current Openings</h2>
                    <ul>
                        <p>We do not have any current openings at this time, thanks so much for your interest!</p>
                    </ul>
                </div>
            </section>
        """
    expected_soup = BeautifulSoup(expected_html, "html.parser")
    expected_openings = expected_soup.select('.openings')[0]

    current_openings_pretty_html = current_openings.prettify(formatter="html")

    return {
        "statusCode": 200,
        "body": json.dumps({
            "current_openings_changed": expected_openings != current_openings,
            "current_openings": current_openings_pretty_html
        })
    }
