## React & Django Project Change log

- Part#2
- created a Room model in models.py with fields code, host, guest_can_pause, votes_to_skip, and created_at
- created the serializers.py file and a RoomSerializer class that translate the Room model into JSON format with desired fields
- created a RoomView class in views.py that allows us to view the list of Rooms and/or add a new Room depending on which rest_framework generics we use

- Part#3
- created a frontend app with folder for all the javascript/react files
- the idea is to have django application render a template, then the react code would take over and fill it in
- installed webpack, babel, react,react-dom, react-router-dom, material-ui, material-ui-icons using npm
- added script file, babel.config.json, which converts codes into codes that would in older browsers, and to use async/await
- added script file, webpack.config.js, which bundles all javascript into one file and server to browser
- set up url endpoint in music_controller/urls.py so a blank url would be route to frontend/urls.py, which then a blank url again would route to the "index" view
- when we run the webpack script with "npm run dev", the script looks at index.js file, bundles all the js files together as one "main.js" in the frontend folder, the file would then be rendered as the frontend "index" view
