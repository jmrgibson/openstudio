import {
    requestClassesClasses as request_classes,
    receiveClassesClasses as receive_classes,
    setClassesClassesLoading as set_loading
} from './actions'

import axios_os from '../../../../utils/axios_os'
import OS_API from '../../../../utils/os_api'
import { toISODate } from '../../../../utils/date_tools'

// just pass these actions as there's nothing else they need to do
// Put pass-through actions here


// data fetchers

const fetchClasses = () => {
      return dispatch => {
          dispatch(request_classes())

          const params = new URLSearchParams()
          const date = new Date()
          const iso_date = toISODate(date)
          params.append('date', iso_date)
          axios_os.post(OS_API.CLASSES_CLASSES, params)
          .then(function (response) {
            // handle success
            dispatch(receive_classes(response.data))
            // dispatch(setLoadingProgress(100))
          })
          .catch(function (error) {
            // handle error
            console.log(error)
            // #TODO: handle error properly


            //history.push('/Uhoh')
            // dispatch(setError(true))
            // dispatch(setErrorMessage("Error loading user data"))
            // if (error.config) {
            //   dispatch(setErrorData(error.config.url))
            // } 
          })
          .then(function () {
            // always executed
          });
      }
  }


export default {
    fetchClasses
}
