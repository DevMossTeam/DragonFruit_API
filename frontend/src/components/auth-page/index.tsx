"use client";
import { AuthPage as AuthPageBase } from "@refinedev/antd";
import type { AuthPageProps } from "@refinedev/core";

export const AuthPage = (props: AuthPageProps) => {
  return ( 
    <AuthPageBase
      type="login"
      title="Dragonfruit Grading"
      formProps={{
        initialValues: { email: "demo@example.com", password: "demodmeo" },
        // onSubmit: async (values) => { /* custom login */ }
      }}
      wrapperProps={{ style: { backgroundImage: "url('/bg.jpg')" } }}
    />
  );
};