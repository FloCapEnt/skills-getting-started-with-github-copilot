"""Tests for the activities endpoints using AAA (Arrange-Act-Assert) pattern."""

import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint."""

    def test_get_activities_returns_all_activities(self, client, reset_activities):
        """
        Arrange: Client is ready
        Act: Send GET request to /activities
        Assert: Returns 200 and contains all activities
        """
        # Arrange
        expected_activity_names = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Basketball Team",
            "Soccer Club",
            "Art Studio",
            "Music Ensemble",
            "Debate Club",
            "Science Olympiad"
        ]

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert len(activities) == 9
        for activity_name in expected_activity_names:
            assert activity_name in activities

    def test_get_activities_returns_activity_details(self, client, reset_activities):
        """
        Arrange: Client is ready
        Act: Send GET request to /activities
        Assert: Each activity contains required fields
        """
        # Arrange
        required_fields = ["description", "schedule", "max_participants", "participants"]

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        activities = response.json()
        for activity_name, details in activities.items():
            for field in required_fields:
                assert field in details, f"Field '{field}' missing from {activity_name}"

    def test_get_activities_includes_participants(self, client, reset_activities):
        """
        Arrange: Client is ready
        Act: Send GET request to /activities
        Assert: Each activity has a participants list
        """
        # Arrange
        # No setup needed

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        activities = response.json()
        chess_club = activities["Chess Club"]
        assert isinstance(chess_club["participants"], list)
        assert len(chess_club["participants"]) == 2
        assert "michael@mergington.edu" in chess_club["participants"]


class TestRootRedirect:
    """Tests for GET / endpoint."""

    def test_root_redirects_to_static_index(self, client, reset_activities):
        """
        Arrange: Client is ready
        Act: Send GET request to /
        Assert: Returns redirect status code
        """
        # Arrange
        # No setup needed

        # Act
        response = client.get("/", follow_redirects=False)

        # Assert
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"
