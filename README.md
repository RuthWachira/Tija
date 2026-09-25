# Tija - A productivity app
Tija is a web application built on Django framework. It is a productivity app that records your long-term and short-term goals spanning across several spheres of life such as career, health, learning, finances etc. It allows you to follow through your goals from creation to completion/abandonment. Tija provides a platform to record little to big successes realised in the achievement of your goals. You also get to record the challenges encountered and their remediation process. 


![Tija illustration banner](https://hgs.cx/wp-content/uploads/2022/11/AgentX-productivity-P2-blog-banner.webp)

## Features 🎯
1. **Goal tracking**: Alows user to set long-term and short-term goals, with specific goal metrics such as category, urgency, and importance. It also tracks progression of the goal, from creation stage to completion/abandonment.
2. **Record wins**: Records specific successes realised in the process of executing a goal, without  limiting it to only completed goals.
3. **Record challenges**: A clear record of challenges faced while executing a goal. Includes remediability of the challenge.
4. **Remediation**: Follows through on the resolution of challenges faced in the execution of the goals.

## Upcoming Features 🎯🎯
1. **Notification center**: Provide reminders and notifications based on specific targets set by the user e.g an alert on an upcoming target completion date for a goal, alert on a stale remediation that has been long standing.
2. **Reporting**:Graphical representation on goal progression, trend reports , patterns and predictions based on current goals.



## Tech stack
- **Backend** : Python (Django)
- **Frontend** : Django templates, CSS(Bootstrap) 
- **Database** : SQLite
- **Deployment** : TBD
- **Version control** : Github
- **API** : Django REST framework

## Installation
1. **Clone the repo**
```bash
git clone https://github.com/RuthWachira/Tija.git 
cd Tija
```
2. **Setting up of virtual environment**
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```
3. **Dependencies**
```bash
pip install -r requirements.txt
```
4. **Migrations**
```bash
python manage.py migrate
```
5. **Starting the development server**
```bash
python manage.py runserver
```
**To get started, visit**: *[local server](http://127.0.0.1:8000/)*

## License
Distributed under the MIT License. See *[LICENSE](LICENSE)* for more information.

## Contact
* created and maintained by: *[Ruth Wachira](https://github.com/RuthWachira)*
* For support, email : *[nyagaki.wachira@gmail.com](mailto:nyagaki.wachira@gmail.com)*
