from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from joblib import load
# from sklearn.preprocessing import StandardScaler
import jsonschema
import numpy as np
import pandas as pd
app = Flask(__name__)

model = load_model("PP_model_4.h5")
scaler = load("scaler_PP_model_4.pkl")

# Load the dataset (if needed for other API functions)
df = pd.read_csv('PPmerged.csv')
df_model = df.drop(columns=['like_id', 'user_id', 'cafe_id'])
df_cafe = pd.read_csv("KafeJakarta.csv")

# LABEL = ["Dislike", "Like"]

@app.route("/")
def index():
    return {"status":"SUCCESS",
            "message":"Service is up"}, 200

@app.route("/home")
def home():
    return {"message":"Welcome Cafe Lovers!"}, 200

@app.route("/palateCheck", methods=["POST"])
def palate_check():
    user_id = request.json["user_id"]
    cafe_id = request.json["cafe_id"]

    # Check if "cafe_id" is present in the JSON and is a string
    if "cafe_id" not in request.json or not isinstance(cafe_id, str):
        raise ValueError("Invalid cafe ID")

    # Validate the cafe ID
    schema = {
        "type": "string",
        "minLength": 1,
        "maxLength": 255
    }
    if not jsonschema.validate(cafe_id, schema):
        raise ValueError("Invalid cafe ID")

    # Convert the cafe ID to a number
    cafe_id_number = int(cafe_id)

    # Preprocess data (similar to your `palateCheck` function)
    user_cafe_data = df_model[(df['user_id'] == user_id) & (df['cafe_id'] == cafe_id_number)].drop(columns=['vote'])
    user_cafe_data_scaled = scaler.transform(user_cafe_data)

    prediction = model.predict(user_cafe_data_scaled)

    return jsonify({"prediction": prediction.tolist()[0]}) # Return the prediction as a list

# Add other API endpoints for palateSearch, palateFilterSearch, etc., using a similar approach

# def palateFilterSearch(Kpopers=0, JapanLovers=0, AnimalLovers=0, Quite=0, 
#                        MusicLovers=0, BookLovers=0, ArtLovers=0, ViewsLovers=0, 
#                        CoffeeLovers=0, NonCoffeeLovers=0, groupsComer=0):
#     kafe_cocok = []
#     for cafe in df_cafe:
#         user_cafe_data = df_model[(df_model['Kpopers'] == Kpopers),
#                                   (df_model['JapanLovers'] == JapanLovers),
#                                   (df_model['AnimalLovers'] == AnimalLovers),
#                                   (df_model['Quite'] == Quite),
#                                   (df_model['MusicLovers'] == MusicLovers),
#                                   (df_model['BookLovers'] == BookLovers),
#                                   (df_model['ArtLovers'] == ArtLovers),
#                                   (df_model['ViewsLovers'] == ViewsLovers),
#                                   (df_model['CoffeeLovers'] == CoffeeLovers),
#                                   (df_model['NonCoffeeLovers'] == NonCoffeeLovers),
#                                   (df_model['groupsComer'] == groupsComer)]
#         user_cafe_data_scaled = scaler.transform(user_cafe_data)
#         prediction = model.predict(user_cafe_data_scaled)
#         if prediction > 0.5:
#             kafe_cocok.append(cafe)
#     return kafe_cocok

# @app.route("/palateFilterSearch", methods=["POST"])
# def palate_filter_search():
#     # Get parameters from JSON request
#     params = request.json
#     Kpopers = params.get("Kpopers", 0)
#     JapanLovers = params.get("JapanLovers", 0)
#     AnimalLovers = params.get("AnimalLovers", 0)
#     Quite = params.get("Quite", 0)
#     MusicLovers = params.get("MusicLovers", 0)
#     BookLovers = params.get("BookLovers", 0)
#     ArtLovers = params.get("ArtLovers", 0)
#     ViewsLovers = params.get("ViewsLovers", 0)
#     CoffeeLovers = params.get("CoffeeLovers", 0)
#     NonCoffeeLovers = params.get("NonCoffeeLovers", 0)
#     groupsComer = params.get("groupsComer", 0)
#     # ... (get other parameters similarly)

#     # Call the function
#     kafe_cocok = palateFilterSearch(Kpopers, JapanLovers, AnimalLovers, Quite,
#                                     MusicLovers, BookLovers, ArtLovers, ViewsLovers,
#                                     CoffeeLovers, NonCoffeeLovers, groupsComer)

#     return jsonify({"kafe_cocok": kafe_cocok})  # Return the list of matching cafes


# @app.route("/sapa")
# def sapa_nama():
#     args = request.args
#     nama = args.get("nama", default="Cafe Lovers")
#     job = args.get("jobtitle", default="Data Analyst")
#     return {"status":"SUCCESS",
#             "message":f"Halo {nama}, your job is {job}"}, 200

# @app.route('/recommendation', methods=['POST'])
# def recommendation():
#     try:

#         data = request.get_json(force=True)
#         input_data = data['user_id']
#         print("Uploaded data:", input_data)
        
#         # input_data = np.array(input_data).reshape(1, -1)
#         input_data_scaled = scaler.transform(input_data)

#         # prediction = model.predict(input_data_scaled)
#         # output = prediction[0][0]

#         recommendation = (model.predict(input_data_scaled) > 0.5).astype(int)
#         result = print(f'Recommendation for User : {recommendation}')

#         return jsonify(result=result)

#     except Exception as e:
#         return str(e), 500

# @app.route("/recommendation")
# def recommendation():
#     args = request.args
#     Kpopers = args.get("Kpopers", default=0)
#     JapanLovers = args.get("JapanLovers", default=0)
#     AnimalLovers = args.get("AnimalLovers", default=0)
#     Quite = args.get("Quite", default=0)
#     MusicLovers = args.get("MusicLovers", default=0)
#     BookLovers = args.get("BookLovers", default=0)
#     ArtLovers = args.get("ArtLovers", default=0)
#     ViewsLovers = args.get("ViewsLovers", default=0)
#     CoffeeLovers = args.get("CoffeeLovers", default=0)
#     NonCoffeeLovers = args.get("NonCoffeeLovers", default=0)
#     groupsComer = args.get("groupsComer", default=0)

#     new_data = [[Kpopers, JapanLovers, AnimalLovers, Quite, MusicLovers, BookLovers, ArtLovers,
#                  ViewsLovers, CoffeeLovers, NonCoffeeLovers, groupsComer]]
#     new_data_scaled = scaler.transform(new_data)
#     recommendation = (model.predict(new_data_scaled) > 0.5).astype(int)
#     result = print(f'Recommendation for User : {recommendation}')
    
#     # result = LABEL[result[0]]

#     return {"status":"SUCCESS",
#             "result":result}, 200

if __name__ == "__main__":
    app.run(debug=True)  # Set debug=True for development