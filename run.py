from flask import Flask, request, redirect
import twilio.twiml
import requests

from api_key import API_KEY
 
app = Flask(__name__)
 
@app.route("/", methods=['GET', 'POST'])
def sms_quote():
    """Respond to incoming requests with a pic and quote"""
 
    # stdout goes to log on Heroku
    print request.values.to_dict()

    color = request.values['Body']

    image_url = get_tshirt_image_url(color)

    if image_url:
        count, price_per = get_quote(color)
        if price_per:
            msg = "%s\nFor %d shirts: %.2f each"%(image_url,
                                                  count,
                                                  price_per)
        else:
            msg = "%s\nError looking up price"%(image_url,)
    else:
        msg = "Couldn't find color: %s"%(color,)
    
    resp = twilio.twiml.Response()
    resp.message(msg)
    return str(resp)
 

def get_tshirt_image_url(color):
    product_id=2
    url = "https://www.shirts.io/api/v1/products/%s/"%(product_id,)

    params = {'api_key': API_KEY}
    r = requests.get(url, params=params)
    if r.status_code == 200:
        result = r.json()['result']
        matching_colors = filter(lambda d: d['name'] == color,
                                 result['colors'])

        if matching_colors:
            image_url = matching_colors[0]['front_image']
        else:
            image_url = None
    else:
        print "Error (%d) looking up tshirt url:\n%s"%(r.status_code,
                                                       r.text)
    return image_url
    

def get_quote(color):
    url = "https://www.shirts.io/api/v1/quote/"
    product_id = 2
    med_count = 100
    lrg_count = 100
    personalization = "Names" # could be Both (for letters and numbers)

    params = {"garment[0][product_id]": product_id,
              "garment[0][color]": color,
              "garment[0][sizes][med]": med_count,
              "garment[0][sizes][lrg]": lrg_count,
              "print[front][color_count]": 1,
              "print[back][color_count]": 1,
              "print_type": "Screenprint",
              "personalization": personalization,
              "api_key": API_KEY,
             }

    r = requests.get(url, params=params)
    print "url:", r.url
    if r.status_code == 200:
        breakdown = r.json()['result']['garment_breakdown']
        count = breakdown['num_shirts']
        price_per = breakdown['price_per_shirt']
    else:
        print "Error (%d) looking up price:\n%s"%(r.status_code,
                                                  r.text)
        count = None
        price_per = None

    return count, price_per

if __name__ == "__main__":
    app.run(debug=True)
