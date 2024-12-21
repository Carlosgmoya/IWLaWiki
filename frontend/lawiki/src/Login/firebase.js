import { GoogleAuthProvider, signInWithPopup, signOut } from "firebase/auth";
import { auth } from "./firebase-config";

const googleProvider = new GoogleAuthProvider();

export const signInWithGoogle = async () => {
    try {
      const result = await signInWithPopup(auth, googleProvider);
      return result.user;
    } catch (error) {
      console.error("Error Inicio de Sesión Google:", error.message);
      throw error;
    }
};
  
export const logout = async () => {
    try {
      await signOut(auth);
    } catch (error) {
      console.error("Error Cierre de Sesión:", error.message);
    }
};