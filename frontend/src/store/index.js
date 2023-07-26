import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate'

const store = new Vuex.Store({
  plugins: [createPersistedState()],
  
  state: {
    between_subject_type: '',
    within_subject_type:'',
    userID: '',
    access_token:'',
    WD_ID: '',
    T_ID: '',
    period: '',
  },
  mutations: {
    setWithinType(state, within) {
      state.within_subject_type = within
    },
    setBetweenType(state, between) {
      state.between_subject_type = between
    },
    setAccessToken(state, access_token) {
      state.access_token = access_token
    },
    setUserID(state, userID) {
      state.userID = userID
    },
    setWD_ID(state, ID) {
      state.WD_ID = ID
    },
    setT_ID(state, ID) {
      state.T_ID = ID
    },
    setPeriod(state, period) {
      state.period = period
    },
  },
  actions: {
    initUserData(context, userData) {
      context.commit("setAccessToken", userData.access_token)
      context.commit("setUserID", userData.userID)
    },
    initExpType(context, expType) {
      context.commit("setWithinType", expType.within)
      context.commit("setBetweenType", expType.between)
    },
    
    initWD_ID(context, ID) {
      context.commit("setWD_ID", ID)
    },
    initT_ID(context, ID) {
      context.commit("setT_ID", ID)
    },

    initPeriod(context, period) {
      context.commit("setPeriod", period)
    }

    // initUserID(context, userID) {
    //   context.commit("setUserID", userID.userID)
    // }

  },
  getters: {
    
  },

  modules: {
    
  }
})

export default store