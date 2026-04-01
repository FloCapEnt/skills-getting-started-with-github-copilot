"""Tests for the signup endpoint using AAA (Arrange-Act-Assert) pattern."""

import pytest


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint."""

    def test_signup_new_participant_successful(self, client, reset_activities):
        """
        Arrange: A new participant email and an activity with available spots
        Act: Send POST request to sign up
        Assert: Returns 200 and confirms the signup
        """
        # Arrange
        activity_name = "Chess Club"
        email = "newtestuser@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_signup_adds_participant_to_activity(self, client, reset_activities):
        """
        Arrange: A new participant email and fresh activity state
        Act: Send POST request to sign up, then fetch activities
        Assert: Participant appears in the activity's participants list
        """
        # Arrange
        activity_name = "Art Studio"
        email = "artlover@mergington.edu"

        # Act
        client.post(f"/activities/{activity_name}/signup", params={"email": email})
        response = client.get("/activities")

        # Assert
        activities = response.json()
        assert email in activities[activity_name]["participants"]

    def test_signup_activity_not_found(self, client, reset_activities):
        """
        Arrange: A non-existent activity name
        Act: Send POST request to sign up
        Assert: Returns 404 with appropriate error message
        """
        # Arrange
        activity_name = "Non-Existent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_signup_duplicate_participant_fails(self, client, reset_activities):
        """
        Arrange: An activity with an existing participant
        Act: Send POST request with the same participant email
        Assert: Returns 400 with duplicate signup error
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already signed up for Chess Club

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "already signed up" in data["detail"]

    def test_signup_different_activities_same_participant(self, client, reset_activities):
        """
        Arrange: A participant signed up for one activity
        Act: Sign up the same participant for a different activity
        Assert: Returns 200 and allows signup to multiple activities
        """
        # Arrange
        email = "multi@mergington.edu"

        # Act - Sign up for first activity
        response1 = client.post(
            "/activities/Chess Club/signup",
            params={"email": email}
        )

        # Act - Sign up for second activity
        response2 = client.post(
            "/activities/Programming Class/signup",
            params={"email": email}
        )

        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200

    def test_signup_with_special_characters_in_email(self, client, reset_activities):
        """
        Arrange: An activity and email with special characters (URL encoded)
        Act: Send POST request with special character email
        Assert: Returns 200 and handles the email correctly
        """
        # Arrange
        activity_name = "Debate Club"
        email = "student+test@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        response_activities = client.get("/activities").json()
        assert email in response_activities[activity_name]["participants"]

    def test_signup_response_message_format(self, client, reset_activities):
        """
        Arrange: A new participant and valid activity
        Act: Send POST request to sign up
        Assert: Response message follows expected format
        """
        # Arrange
        activity_name = "Music Ensemble"
        email = "musician@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == f"Signed up {email} for {activity_name}"
