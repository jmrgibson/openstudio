import React, { Component } from 'react';

import {
  HashRouter as Router,
  Route, 
  Switch
} from 'react-router-dom';


import Cashbook from './cashbook/Cashbook'
import ExpenseAdd from './cashbook/ExpenseAddContainer'
import ExpenseEdit from './cashbook/ExpenseEditContainer'
import CashCountSet from './cashbook/CashCountSetContainer'
import Customers from './customers/list/CustomersContainer'
import Classes from './classes/classes/ClassesContainer'
import Attendance from './classes/attendance/AttendanceContainer'
import Book from './classes/book/BookContainer'
import Revenue from './classes/revenue/RevenueContainer'
import Home from './home/HomeContainer'
import CustomItem from './shop/custom/CustomItemContainer'
import Payment from './shop/payment/PaymentContainer'
import Products from './shop/products/ProductsContainer'
import Classcards from './shop/school/classcards/ClasscardsContainer'
import Memberships from './shop/school/memberships/MembershipsContainer'
import Subscriptions from './shop/school/subscriptions/SubscriptionsContainer'
import Validation from './shop/validation/ValidationContainer'
import PermissionsError from './permissions_error/PermissionsErrorContainer'
import Whoops404 from './whoops404/Whoops404'
import LoadingScreen from '../components/ui/LoadingScreen'

import '../../stylesheets/app/App.scss'

class App extends Component {
  constructor(props) {
    super(props)
    console.log(this.props)
  }

  componentWillMount() {
    this.props.fetchClasses()
    this.props.fetchPaymentMethods()
    this.props.fetchTaxRates()
    this.props.fetchProductCategories()
    this.props.fetchUser()    
    this.props.fetchSettings()  
    this.props.fetchCustomers()
    this.props.fetchCustomersClasscards()
    this.props.fetchCustomersSubscriptions()
    this.props.fetchCustomersMemberships()
    this.props.fetchCustomersMembershipsToday()
    this.props.fetchCashCounts()
    this.props.fetchExpenses()
    this.props.fetchShopProducts()
    this.props.fetchShopSchoolClasscards()
    this.props.fetchShopSchoolMemberships()
    this.props.fetchShopSchoolSubscriptions()
  }

  render() {
    return (
      (this.props.app_state.loading) ? 
        <LoadingScreen progress={this.props.app_state.loading_progress}
        message={this.props.app_state.loading_message}/> :
      <Router>
          <Switch>
            <Route exact path='/' component={Customers} />
            <Route exact path='/classes' component={Classes} />
            <Route exact path='/classes/:customerID' component={Classes} />
            <Route path='/classes/attendance/:clsID' component={Attendance} />
            <Route path='/classes/book/:customerID/:classID' component={Book} />
            <Route path='/classes/revenue/:clsID' component={Revenue} />
            <Route path='/customers' component={Customers} />
            <Route exact path='/cashbook' component={Cashbook} />
            <Route path='/cashbook/expenses/add' component={ExpenseAdd} />
            <Route path='/cashbook/expenses/edit/:eID' component={ExpenseEdit} />
            <Route path='/cashbook/cashcount/set/:type' component={CashCountSet} />
            <Route path="/shop/payment" component={Payment} />
            <Route path="/shop/validation" component={Validation} />
            <Route exact path='/shop/products' component={Products} />
            <Route path='/shop/school/classcards' component={Classcards} />
            <Route path='/shop/school/memberships' component={Memberships} />
            <Route path='/shop/school/subscriptions' component={Subscriptions} />
            <Route path='/shop/custom' component={CustomItem} />
            <Route path='/permissions_error' component={PermissionsError} />
            {/* Add all your remaining routes here, like /trending, /about, etc. */}
            <Route component={Whoops404} />
          </Switch>
      </Router>
    )
  }
}

export default App