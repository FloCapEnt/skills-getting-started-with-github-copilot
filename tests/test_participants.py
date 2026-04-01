"""Tests for the participant removal endpoint using AAA (Arrange-Act-Assert) pattern."""

import pytest


class TestRemoveParticipant:
    """Tests for DELETE /activities/{activity_name}/participants/{email} endpoint."""

    def test_remove_participant_successful(self, client, reset_activities):
        """
        Arrange: An activity with an existing participant
        Act: Send DELETE request to remove the participant
        Assert: Returns 200 and confirms the removal
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_remove_participant_from_activity_list(self, client, reset_activities):
        """
        Arrange: An activity with existing participants
        Act: Delete a participant, then fetch activities
        Assert: Participant no longer appears in the activity's list
        """
        # Arrange
        activity_name = "Soccer Club"
        email = "lucas@mergington.edu"

        # Act
        client.delete(f"/activities/{activity_name}/participants/{email}")
        response = client.get("/activities")

        # Assert
        activities = response.json()
        assert email not in activities[activity_name]["participants"]
        assert "sophia@mergington.edu" in activities[activity_name]["participants"]

    def test_remove_participant_decreases_count(self, client, reset_activities):
        """
        Arrange: An activity with multiple participants
        Act: Delete a participant and check participant count
        Assert: Participant count decreased by one
        """
        # Arrange
        activity_name = "Chess Club"
        email_to_remove = "michael@mergington.edu"

        # Act
        response_before = client.get("/activities").json()
        count_before = len(response_before[activity_name]["participants"])

        client.delete(f"/activities/{activity_name}/participants/{email_to_remove}")
        response_after = client.get("/activities").json()
        count_after = len(response_after[activity_name]["participants"])

        # Assert
        assert count_before - count_after == 1

    def test_remove_participant_activity_not_found(self, client, reset_activities):
        """
        Arrange: A non-existent activity name
        Act: Send DELETE request to remove participant
        Assert: Returns 404 with activity not found error
        """
        # Arrange
        activity_name = "Non-Existent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_remove_nonexistent_participant(self, client, reset_activities):
        """
        Arrange: An activity and a participant not in that activity
        Act: Send DELETE request to remove non-existent participant
        Assert: Returns 404 with participant not found error
        """
        # Arrange
        activity_name = "Chess Club"
        email = "nonexistent@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "Participant not found" in data["detail"]

    def test_remove_same_participant_twice_fails_second_time(self, client, reset_activities):
        """
        Arrange: An activity with a participant
        Act: Delete the participant twice
        Assert: First delete succeeds, second fails with 404
        """
        # Arrange
        activity_name = "Debate Club"
        email = "benjamin@mergington.edu"

        # Act - First deletion
        response1 = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )

        # Act - Second deletion (should fail)
        response2 = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )

        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 404

    def test_remove_participant_response_format(self, client, reset_activities):
        """
        Arrange: An activity with a participant
        Act: Send DELETE request
        Assert: Response message follows expected format
        """
        # Arrange
        activity_name = "Art Studio"
        email = "isabella@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == f"Removed {email} from {activity_name}"

    def test_remove_participant_with_special_characters(self, client, reset_activities):
        """
        Arrange: A participant with special characters in email already signed up
        Act: First sign up with special email, then delete
        Assert: Successfully removes the participant
        """
        # Arrange
        activity_name = "Science Olympiad"
        email = "student+test@mergington.edu"
        
        # First sign up the participant
        client.post(f"/activities/{activity_name}/signup", params={"email": email})

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )

        # Assert
        assert response.status_code == 200
        response_activities = client.get("/activities").json()
        assert email not in response_activities[activity_name]["participants"]

    def test_remove_only_participant_from_activity(self, client, reset_activities):
        """
        Arrange: An activity with only one participant
        Act: Delete that participant
        Assert: Activity's participant list becomes empty
        """
        # Arrange
        activity_name = "Basketball Team"
        email = "james@mergington.edu"  # Only participant

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )

        # Assert
        assert response.status_code == 200
        response_activities = client.get("/activities").json()
        assert len(response_activities[activity_name]["participants"]) == 0
