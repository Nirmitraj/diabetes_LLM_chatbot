(function() {
    document.addEventListener('DOMContentLoaded', () => {
        const accessToken = sessionStorage.getItem('accessToken');
        const userId = sessionStorage.getItem('userId');
        if (accessToken && userId) {
            load_profile_data(userId, accessToken);
        }
      });
      
    async function get_profile_data(userId, accessToken) {
        const url = baseURL + '/user/' + userId
      
        try {
            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + accessToken

                }
            });      
            if (!response.ok) {
                sessionStorage.removeItem('accessToken');
                sessionStorage.removeItem('email');
                sessionStorage.removeItem('userId');
                alert("Session expired, relogin to continue.");

                window.location.href = 'login.html';
            }
      
            const data = await response.json();
            return data
        } catch (error) {
            console.error('There has been a problem with your fetch operation:', error);
        }
    }

    async function load_profile_data(userId, accessToken){
        profile_data = await get_profile_data(userId, accessToken);
        
        prefix = 'profile_'
        fullname = document.getElementById(prefix + "fullname");
        sex = document.getElementById(prefix + "sex");
        age = document.getElementById(prefix + "age");
        diagnose_date = document.getElementById(prefix + "diagnose_date");
        glucose_level = document.getElementById(prefix + "glucose_level");
        other_medical_conditions = document.getElementById(prefix + "other_medical_conditions");
        diet = document.getElementById(prefix + "diet");
        height = document.getElementById(prefix + "height");
        physical_level = document.getElementById(prefix + "physical_level");
        weight = document.getElementById(prefix + "weight");
        management_goals = document.getElementById(prefix + "management_goals");
        learning_preference = document.getElementById(prefix + "learning_preference");

        fullname.value = profile_data.user['full_name'];
        age.value = profile_data.user['age'];
        diagnose_date.valueAsDate = new Date(profile_data.user['diagnose_date']);
        glucose_level.value = profile_data.user['blood_glucose_level'];
        other_medical_conditions.value = profile_data.user['medical_conditions'];
        height.value = profile_data.user['height'];
        weight.value = profile_data.user['weight'];
        physical_level.value = profile_data.user['physical_activity'];
        management_goals.value = profile_data.user['management_goals'];
        learning_preference.value = profile_data.user['learning_preference'];


        sex_value = profile_data.user['gender'].toLowerCase();
        if (sex_value == "male"){
            sex.selectedIndex = 1
        }else if (sex_value == "female"){
            sex.selectedIndex = 2
        }else{
            sex.selectedIndex = 3
        }

        diet_value = profile_data.user['dietary_pref'].toLowerCase();
        if (diet_value == "vegetarian"){
            diet.selectedIndex = 1
        }else if (diet_value == "vegan"){
            diet.selectedIndex = 2
        }else if (diet_value == "glutenfree"){
            diet.selectedIndex = 3
        }else if (diet_value == "kosher"){
            diet.selectedIndex = 4
        }else{
            diet.selectedIndex = 5
        }
    }
})();

function extract_profile_data(){
    prefix = 'profile_';
    data = {}

    fullname = document.getElementById(prefix + "fullname");
    sex = document.getElementById(prefix + "sex");
    age = document.getElementById(prefix + "age");
    diagnose_date = document.getElementById(prefix + "diagnose_date");
    glucose_level = document.getElementById(prefix + "glucose_level");
    other_medical_conditions = document.getElementById(prefix + "other_medical_conditions");
    diet = document.getElementById(prefix + "diet");
    height = document.getElementById(prefix + "height");
    physical_level = document.getElementById(prefix + "physical_level");
    weight = document.getElementById(prefix + "weight");
    management_goals = document.getElementById(prefix + "management_goals");
    learning_preference = document.getElementById(prefix + "learning_preference");

    data['full_name'] = fullname.value;
    data['age'] = age.value;
    data['diagnose_date'] = diagnose_date.value;
    data['blood_glucose_level'] = glucose_level.value;
    data['medical_conditions'] = other_medical_conditions.value;
    data['height'] = height.value;
    data['weight'] = weight.value;
    data['physical_activity'] = physical_level.value;
    data['management_goals'] = management_goals.value;
    data['learning_preference'] = learning_preference.value;
    data['gender'] = sex.options[sex.selectedIndex].text;
    data['dietary_pref'] = diet.options[diet.selectedIndex].text;

    return data
}

async function update_user_profile(event){
    event.preventDefault();
        
    
    
    const accessToken = sessionStorage.getItem('accessToken');
    const userId = sessionStorage.getItem('userId');
    const url = baseURL + '/user/' + userId;
      
    try {
        const response = await fetch(url, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + accessToken

            },
            body: JSON.stringify(extract_profile_data()),
        });      
        if (!response.ok) {
            console.error('There has been a problem with your fetch operation:', error);
        }

        message = document.getElementById('update_message');
        message_container = document.getElementById('update_message_container');

        message_container.classList.remove('hide');
        message_container.classList.add('show');
        message.innerText = 'Your data is updated!';
        return
    } catch (error) {
        console.error('There has been a problem with your fetch operation:', error);
    }
}

function dismissAlert() {
    var alertContainer = document.getElementById('update_message_container');
    alertContainer.classList.remove('show');
    alertContainer.classList.add('hide');
}