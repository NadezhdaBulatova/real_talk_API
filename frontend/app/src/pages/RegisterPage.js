import Layout from "../components/Layout";
import {
  useRegisterMutation,
  useLoginMutation,
  useUserQuery,
} from "../services/auth";

const RegisterPage = () => {
  const username = "user8";
  const password = "1234QWer!";
  const email = "user8@example.com";
  const [
    register,
    { isLoading, data: registerData, error: registerError }, // This is the destructured mutation result
  ] = useRegisterMutation();

  const [login, { data: loginData, error: loginError }] = useLoginMutation();

  const { data: userData, error: userError } = useUserQuery(2);

  console.log("****ERRROR", userData);
  console.log("****SUCCESS", userError);
  return (
    <Layout>
      <div>Register Page</div>
      <button
        className="w-48 h-48 bg-red-800"
        onClick={() => {
          register({
            email,
            password,
            username,
          });
        }}
      >
        Register
      </button>
      <button
        className="w-48 h-48 bg-green-800"
        onClick={() => {
          login({
            email,
            password,
          });
        }}
      >
        Register
      </button>
    </Layout>
  );
};

export default RegisterPage;
