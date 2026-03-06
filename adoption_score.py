def get_yes_no(prompt):
    while True:
        answer = input(prompt).strip().lower()
        if answer in ["yes", "y"]:
            return "yes"
        elif answer in ["no", "n"]:
            return "no"
        print("Invalid input. Please enter 'yes' or 'no'.")


def get_choice(prompt, choices):
    choices_lower = [c.lower() for c in choices]
    while True:
        answer = input(prompt).strip().lower()
        if answer in choices_lower:
            return answer
        print(f"Invalid input. Please choose from: {', '.join(choices)}")


def get_int(prompt, min_val=0, max_val=None):
    while True:
        try:
            value = int(input(prompt))
            if value < min_val:
                print(f"Invalid input. Value must be at least {min_val}.")
                continue
            if max_val is not None and value > max_val:
                print(f"Invalid input. Value must be no greater than {max_val}.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a whole number.")


def get_float(prompt, min_val=0, max_val=None):
    while True:
        try:
            value = float(input(prompt))
            if value < min_val:
                print(f"Invalid input. Value must be at least {min_val}.")
                continue
            if max_val is not None and value > max_val:
                print(f"Invalid input. Value must be no greater than {max_val}.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a number.")


def adoption_score():

    score = 10
    declined = False
    reason = ""
    deductions = []

    print("\nCat Adoption Interview Scoring\n")

    # 0 Number of adult adopters
    num_adults = get_int("How many adult adopters will there be? ", 1)

    # 1 Housing
    housing = get_choice("Do you own or rent? (own/rent): ", ["own", "rent"])
    if housing == "rent":
        score -= 1
        deductions.append(("Renting home", -1))

    # 2 Out-of-state check
    out_of_state = get_yes_no("Are you adopting from out of state? ")
    if out_of_state == "yes":
        declined = True
        reason = "Applicant is out of state"
        print("\n----- RESULT -----")
        print("Status: DECLINED")
        print("Reason:", reason)
        return

    # 3 Distance within state
    distance = get_float("How many hours away do you live? (0–8 allowed): ", 0)
    if distance > 8:
        declined = True
        reason = "Distance over 8 hours"
        print("\n----- RESULT -----")
        print("Status: DECLINED")
        print("Reason:", reason)
        return

    # Distance scoring
    if 1 <= distance < 1.5:
        score -= 0.5
        deductions.append(("Distance 1–1.5 hrs", -0.5))
    elif 1.5 <= distance <= 2:
        score -= 1
        deductions.append(("Distance 1.5–2 hrs", -1))
    elif distance > 2:
        score -= 2
        deductions.append(("Distance 2–8 hrs", -2))

    # 4 Children
    kitten = get_yes_no("Are you adopting a kitten? ")
    child_under8 = get_yes_no("Is there a child under 8 in the home? ")
    if kitten == "yes" and child_under8 == "yes":
        declined = True
        reason = "Young child with kitten adoption"
    elif kitten == "no" and child_under8 == "yes":
        score -= 0.5
        deductions.append(("Child under 8 in home", -0.5))

    # 5 Other pets
    pets = get_choice("Any other pets? (none/cats/dogs): ", ["none", "cats", "dogs"])
    if pets != "none":
        if pets == "cats":
            good_with_cats = get_yes_no("Is the cat good with other cats? ")
            if good_with_cats == "no":
                declined = True
                reason = "Cat cannot live with other cats"
                print("\n----- RESULT -----")
                print("Status: DECLINED")
                print("Reason:", reason)
                return

            # Number of cats currently
            num_cats = get_int("How many cats are currently in the home? ", 0)

            # Legal maximum: 5 cats total
            if num_cats + 1 > 5:
                declined = True
                reason = f"Adopting a cat would exceed legal limit of 5 cats (currently {num_cats})"
                print("\n----- RESULT -----")
                print("Status: DECLINED")
                print("Reason:", reason)
                return

            # 2 per adult rule: if current cats ≥ 2*adults → -2 points
            max_by_adult = 2 * num_adults
            if num_cats >= max_by_adult:
                score -= 2
                deductions.append((f"Too many cats for {num_adults} adult(s)", -2))

        elif pets == "dogs":
            good_with_dogs = get_yes_no("Is the cat good with dogs? ")
            if good_with_dogs == "no":
                declined = True
                reason = "Cat cannot live with dogs"
                print("\n----- RESULT -----")
                print("Status: DECLINED")
                print("Reason:", reason)
                return

    # 6 Dog temperament
    if pets == "dogs":
        activity = get_choice("Dog activity level? (low/medium/high): ", ["low", "medium", "high"])
        if activity == "low":
            score -= 0.5
            deductions.append(("Low activity dog", -0.5))
        elif activity == "medium":
            score -= 1
            deductions.append(("Medium activity dog", -1))
        elif activity == "high":
            score -= 2
            deductions.append(("High activity dog", -2))

    # 7 Alone time
    hours = get_int("How many hours would the cat be alone per day?: ", 0, 24)
    if hours == 9:
        score -= 0.5
        deductions.append(("Cat alone 9 hours", -0.5))
    elif hours == 10:
        score -= 1
        deductions.append(("Cat alone 10 hours", -1))
    elif hours >= 11:
        score -= 2
        deductions.append(("Cat alone 11+ hours", -2))

    # 8 Allergies → immediate decline
    allergy = get_yes_no("Any cat allergies in the home? ")
    if allergy == "yes":
        declined = True
        reason = "Cat allergy in household"
        print("\n----- RESULT -----")
        print("Status: DECLINED")
        print("Reason:", reason)
        return

    # 9 Declawing → immediate decline
    declaw = get_yes_no("Would you ever declaw the cat? ")
    if declaw == "yes":
        declined = True
        reason = "Declawing intention"
        print("\n----- RESULT -----")
        print("Status: DECLINED")
        print("Reason:", reason)
        return

    # 10 Outdoor access → immediate decline
    outside = get_yes_no("Would the cat go outside at all? ")
    if outside == "yes":
        declined = True
        reason = "Outdoor access planned"
        print("\n----- RESULT -----")
        print("Status: DECLINED")
        print("Reason:", reason)
        return

    # 11 Age
    age = get_int("Age of adopter: ", 18, 120)
    if kitten == "yes" and age > 68:
        declined = True
        reason = "Age over 68 for kitten adoption"
    if age > 80:
        declined = True
        reason = "Adopter age over 80"
    if 66 <= age <= 75:
        score -= 0.5
        deductions.append(("Age 66–75", -0.5))
    elif 76 <= age <= 80:
        score -= 1
        deductions.append(("Age 76–80", -1))

    # Final result
    print("\n----- RESULT -----")
    if declined:
        print("Status: DECLINED")
        print("Reason:", reason)
    else:
        print(f"Final Score: {score}")
        print("\nScore Breakdown:")
        if deductions:
            for item, pts in deductions:
                print(f"{item}: {pts}")
        else:
            print("No deductions applied.")
        if score < 5.5:
            print("\nStatus: Not approved (below 5.5)")
        elif score < 7:
            print("\nStatus: Borderline – needs review")
        else:
            print("\nStatus: Approved candidate")


# Main loop
while True:
    adoption_score()
    again = get_yes_no("\nWould you like to run another interview? ")
    if again == "no":
        break

print("\nProgram ended.")
input("Press Enter to exit...")