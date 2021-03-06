import { combineReducers } from 'redux';
import listReducer from './list/duck'
import customersClasscardsReducer from './classcards/duck'
import customersSubscriptionsReducer from './subscriptions/duck'
import customersMembershipsReducer from './memberships/duck'
import customersMembershipsTodayReducer from './memberships_today/duck'

const customersReducer = combineReducers({
  list: listReducer,
  classcards: customersClasscardsReducer,
  subscriptions: customersSubscriptionsReducer,
  memberships: customersMembershipsReducer,
  memberships_today: customersMembershipsTodayReducer
})

export default customersReducer