__all__ = ['pet_breeds', 'pet_records']

def pet_breeds(results):
    breeds = []
    for breed in results.find("breeds"):
        breeds.append(breed.text)
    return breeds

def pet_record(results, return_type):
    record = {}
    if return_type == "id":
        return results.find("petIds/id").text
    record["Age"] = results.find("pet/age").text
    record["Breed"] = results.find("pet/breeds/breed").text
    record["Mix"] = results.find("pet/mix").text
    record["Name"] = results.find("pet/name").text
    record["Pet_ID"] = results.find("pet/id").text
    record["Sex"] = results.find("pet/sex").text
    record["Shelter_ID"] = results.find("pet/shelterId").text
    record["Size"] = results.find("pet/size").text

    # Get all contact
    record["Address1"] = results.find("pet/contact/address1").text
    record["Address2"] = results.find("pet/contact/address2").text
    record["City"] = results.find("pet/contact/city").text
    record["State"] = results.find("pet/contact/state").text
    record["Zip"] = results.find("pet/contact/zip").text
    record["Phone"] = results.find("pet/contact/phone").text
    record["Fax"] = results.find("pet/contact/fax").text
    record["Email"] = results.find("pet/contact/email").text

    # Get all media
    record["Image_URL"] = []
    try:
        for image_url in results.find("pet/media/photos/photo"):
            record["Image_URL"].append(image_url)
    except:
        pass

    # If return_type is full, get description of pet
    if return_type == "full":
        record["Description"] = results.find("pet/description").text
    return record

def pet_records(results, return_type):
    records = []
    for pet in results.findall("pets/pet"):
        record = {}
        record["Age"] = pet.find("age").text
        record["Breed"] = pet.find("breeds/breed").text
        record["Mix"] = pet.find("mix").text
        record["Name"] = pet.find("name").text
        record["Pet_ID"] = pet.find("id").text
        record["Sex"] = pet.find("sex").text
        record["Shelter_ID"] = pet.find("shelterId").text
        record["Size"] = pet.find("size").text

        # Get all contact
        record["Address1"] = pet.find("contact/address1").text
        record["Address2"] = pet.find("contact/address2").text
        record["City"] = pet.find("contact/city").text
        record["State"] = pet.find("contact/state").text
        record["Zip"] = pet.find("contact/zip").text
        record["Phone"] = pet.find("contact/phone").text
        record["Fax"] = pet.find("contact/fax").text
        record["Email"] = pet.find("contact/email").text

        # Get all media
        record["Image_URL"] = []
        try:
            for image_url in pet.find("media/photos/photo"):
                record["Image_URL"].append(image_url)
        except:
            pass

        # If return_type is full, get description of pet
        if return_type == "full":
            record["Description"] = pet.find("description").text

        records.append(record)
    return records
