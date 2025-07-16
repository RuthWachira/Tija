# Tija - A productivity app
Tija is a web application built on Django framework. It is productivity app that aims to track the efficiency your daily productive activities such as work, learning etc.
It also tracks progress of your long-term and short-term goals.

![Tija illustration banner](https://hgs.cx/wp-content/uploads/2022/11/AgentX-productivity-P2-blog-banner.webp)

## Features 🎯
1. **Goal tracking**: For setting long-term and short-term goals.
2. **Engaged time**: Records actual start and stops of productive work/activity hours.
3. **Breaks and recharge**: Tracks breaks and recharge time taken.
4. **Sleep hygiene monitor**: Tracks daily sleep hours.
5. **Reporting**: Reports on the daily productivity scale, indicating the impact therein of the other key metrics affecting productivity such as sleep and recharge time.
In the long term, daily habits over time are used to report on  Goal achievement, prediction of a goal being achieved based on target set and actual daily habits to date.
6. **Notification center** (upcoming feature): provide reminders and notifications based on specific targets set by user e.g an alert on desired start time for work hours, alert on desired sleep time.

## Tech stack
- **Backend** : Python (Django)
- **Frontend** : HTML, CSS(Bootstrap) 
- **Database** : MySQL
- **Deployment** : Heroku
- **Version control** : Git
- **API** : Django REST framework

## Installation
1. **Clone the repo**
'''bash
git clone https://github.com/RuthWachira/Tija.git 
cd Tija
'''
2. **Setting up of virtual environment**
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
3. **Dependencies**
'''bash
pip install -r requirements.txt
'''
4. **Migrations**
''' bash
'python manage.py migrate'

5. **Starting the development server**
'''bash
python manage.py runserver
'''
**To get started, visit**: *[local server](http://127.0.0.1:8000/)*

## License
Distributed under the MIT License. See *[LICENSE](LICENSE)* for more information.

## Contact
* created and maintained by: *[Ruth Wachira](https://github.com/RuthWachira)*
* For support, email : *[nyagaki.wachira@gmail.com](mailto:nyagaki.wachira@gmail.com)*
