from settings import environment


def get_register_pass_sms_template(name, url_code):
    if name == '':
        name = 'there'
    elif len(name) > 20:
        name = name.split(' ')[0]

    if environment == 'dev':
        url = 'http://dev.orlemyouthweek.in/ticket/' + url_code
    elif environment == 'stag':
        url = 'http://stag.orlemyouthweek.in/ticket/' + url_code
    elif environment == 'prod':
        url = 'https://orlemyouthweek.in/ticket/' + url_code
    else:
        url = ''

    register_pass_sms_template = """Hi #name,
Your ticket(s) for Orlem Youth Week 2019 is successfully booked.

Please show this QR code #url while entering. All details regarding your ticket(s) are available on the link.

Regards,
OYW 2019"""

    register_pass_sms_template = register_pass_sms_template.replace(
        '#name', name)
    register_pass_sms_template = register_pass_sms_template.replace(
        '#url', url)

    return register_pass_sms_template


def get_accept_pass_sms_template(my_pass, volunteer):

    accept_pass_sms_template = """Hey #name,
Your ticket(s) for OYW was redeemed today by #volunteer.
 
Balance
Weekday x #days
Weekend x #ends
Week(for today) x #weeks
 
Regards,
OYW 2019"""
    accept_pass_sms_template = accept_pass_sms_template.replace(
        '#name', my_pass.name)
    accept_pass_sms_template = accept_pass_sms_template.replace(
        '#volunteer', volunteer)
    accept_pass_sms_template = accept_pass_sms_template.replace(
        '#days', str(my_pass.days))
    accept_pass_sms_template = accept_pass_sms_template.replace(
        '#ends', str(my_pass.ends))
    accept_pass_sms_template = accept_pass_sms_template.replace(
        '#weeks', str(my_pass.weeks - my_pass.weekscanned))

    return accept_pass_sms_template


def get_sms_for_newly_created_volunteer(name):

    welcome_message = """Hey #name,
Your account for Orlem Youth Week is created!
Log in on #url"""

    url = ''
    if environment == 'dev':
        url = 'http://dev.orlemyouthweek.in'
    elif environment == 'stag':
        url = 'http://stag.orlemyouthweek.in'
    elif environment == 'prod':
        url = 'https://orlemyouthweek.in'
    else:
        url = ''

    welcome_message = welcome_message.replace('#name', name)
    welcome_message = welcome_message.replace('#url', url)

    return welcome_message

