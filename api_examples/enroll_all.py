import requests
base_url = 'http://127.0.0.1:8000/api/'

#retriever all courses
r = requests.get(f'{base_url}courses')
courses = r.json()
available_courses = ", ".join([course['title'] for course in courses])
print(f'Available courses: {available_courses}')