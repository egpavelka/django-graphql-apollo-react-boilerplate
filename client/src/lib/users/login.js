import { useMutation } from '@apollo/client'
import Cookies from '../utils/cookies'
import TOKEN_AUTH from '../graphql/mutations/TokenAuth.graphql'

export const useLoginMutation = () => {

  const [login, loginResult] = useMutation(TOKEN_AUTH, {
    onCompleted: data => {
      Cookies.set({}, 'JWT', data.tokenAuth.token)
    },
  })

  return [login, loginResult]
}
