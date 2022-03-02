import Vuex from 'vuex'
import class_num_dict from './class_num'


function get_exp_type() {
  var choosable_lst = [];
  var min_class_num = Math.min(...Object.values(class_num_dict))


  for(var i in Object.keys(class_num_dict)) {
    if(class_num_dict[i] == min_class_num) {
      choosable_lst.push(i)
    }
  }

  var current_class = choosable_lst[Math.floor(Math.random()*choosable_lst.length)]
  var between_subject_type = 0
  var within_subject_type = 0

  if(current_class < 4) {
    between_subject_type = 0
    within_subject_type = current_class
  } else {
    between_subject_type = 1
    within_subject_type = current_class-4
  }

  return [between_subject_type, within_subject_type]
}

const store = new Vuex.Store({
  state: {
    between_subject_type: 0,
    within_subject_type:0,
    access_token:0,
    pass_exp_num: 0,
  },
  mutations: {
    initial_exp_type() {
      var result = get_exp_type()
      store.between_subject_type = result[0]
      store.within_subject_type = result[1]
    }
  },
  actions: {

  },
  modules: {
    
  }
})

export default store