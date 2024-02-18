/**
 * Traverse state from ui-router to find at the current state level or in a parent the specified property.
 * @param currentState (requires $state.$current)
 * @param property
 */
function getPropertyFromStateHierachy(currentState, property) {
	if(!currentState) {
		return null;
	}

	if(currentState.self[property]) {
		return currentState.self[property];
	} else {
		return getPropertyFromStateHierachy(currentState.parent, property);
	}
}