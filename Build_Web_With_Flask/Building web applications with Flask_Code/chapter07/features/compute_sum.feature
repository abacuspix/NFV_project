Feature: compute sum
	In order to compute a sum
	As student
	Implement sum_fnc
	Scenario: Sum of positives
		Given I have the numbers 10 and 20
		When I sum them
		Then I see the result 30
	Scenario: Sum of negatives
		Given I have the numbers -10 and -20
		When I sum them
		Then I see the result -30
	Scenario: Sum with mixed signals
		Given I have the numbers 10 and -20
		When I sum them
		Then I see the result -10