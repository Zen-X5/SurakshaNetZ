"use client";

import { Form, Input, Button, Select, Checkbox, message } from "antd";
import {
    UserOutlined,
    MailOutlined,
    LockOutlined,
    PhoneOutlined,
} from "@ant-design/icons";
import { useRouter } from "next/navigation";
import { useRegisterMutation } from "@/lib/services/api";

const { Option } = Select;

export default function RegisterPage() {
    const [form] = Form.useForm();
    const router = useRouter();
    const [register, { isLoading }] = useRegisterMutation();

    const handleSubmit = async (values: any) => {
        try {
            const payload = {
                displayName: values.name,
                email: values.email,
                phoneNumber: values.phone,
                password: values.password,
            };

            const res = await register(payload).unwrap();
            message.success(res.message || "Account created successfully!");
            router.push("/auth/login");
        } catch (err: any) {
            const errorMsg = err?.data?.message || "Registration failed. Please try again.";
            message.error(errorMsg);
        }
    };

    return (
        <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4 py-10">
            <div className="w-full max-w-md rounded-2xl bg-white p-8 shadow-lg">

                {/* Header */}
                <div className="mb-8 text-center">
                    <h1 className="text-3xl font-bold text-gray-900">
                        Create Account
                    </h1>

                    <p className="mt-2 text-sm text-gray-500">
                        Register your account to get started
                    </p>
                </div>

                {/* Register Form */}
                <Form
                    form={form}
                    layout="vertical"
                    onFinish={handleSubmit}
                    requiredMark={false}
                >
                    {/* Full Name */}
                    <Form.Item
                        label="Full Name"
                        name="name"
                        rules={[
                            { required: true, message: "Please enter your full name" },
                        ]}
                    >
                        <Input
                            size="large"
                            prefix={<UserOutlined />}
                            placeholder="Enter your full name"
                        />
                    </Form.Item>

                    {/* Email */}
                    <Form.Item
                        label="Email"
                        name="email"
                        rules={[
                            { required: true, message: "Please enter your email" },
                            {
                                type: "email",
                                message: "Please enter a valid email",
                            },
                        ]}
                    >
                        <Input
                            size="large"
                            prefix={<MailOutlined />}
                            placeholder="Enter your email"
                        />
                    </Form.Item>

                    {/* Phone */}
                    <Form.Item
                        label="Phone Number"
                        name="phone"
                        rules={[
                            { required: true, message: "Please enter your phone number" },
                        ]}
                    >
                        <Input
                            size="large"
                            prefix={<PhoneOutlined />}
                            placeholder="Enter your phone number"
                        />
                    </Form.Item>

                    {/* Password */}
                    <Form.Item
                        label="Password"
                        name="password"
                        rules={[
                            { required: true, message: "Please enter your password" },
                            {
                                min: 6,
                                message: "Password must be at least 6 characters",
                            },
                        ]}
                    >
                        <Input.Password
                            size="large"
                            prefix={<LockOutlined />}
                            placeholder="Enter your password"
                        />
                    </Form.Item>

                    {/* Confirm Password */}
                    <Form.Item
                        label="Confirm Password"
                        name="confirmPassword"
                        dependencies={["password"]}
                        rules={[
                            {
                                required: true,
                                message: "Please confirm your password",
                            },
                            ({ getFieldValue }) => ({
                                validator(_, value) {
                                    if (!value || getFieldValue("password") === value) {
                                        return Promise.resolve();
                                    }

                                    return Promise.reject(
                                        new Error("Passwords do not match")
                                    );
                                },
                            }),
                        ]}
                    >
                        <Input.Password
                            size="large"
                            prefix={<LockOutlined />}
                            placeholder="Confirm your password"
                        />
                    </Form.Item>

                    {/* Terms */}
                    <Form.Item
                        name="terms"
                        valuePropName="checked"
                        rules={[
                            {
                                validator: (_, value) =>
                                    value
                                        ? Promise.resolve()
                                        : Promise.reject(
                                            new Error("Please accept the terms and conditions")
                                        ),
                            },
                        ]}
                    >
                        <Checkbox>
                            I agree to the Terms & Conditions
                        </Checkbox>
                    </Form.Item>

                    {/* Submit */}
                    <Form.Item>
                        <Button
                            type="primary"
                            htmlType="submit"
                            size="large"
                            block
                            className="!h-12 !rounded-lg !text-base !font-semibold"
                        >
                            Create Account
                        </Button>
                    </Form.Item>
                </Form>

                {/* Login */}
                <p className="text-center text-sm text-gray-500">
                    Already have an account?{" "}
                    <a
                        href="/login"
                        className="font-semibold text-blue-600 hover:text-blue-700"
                    >
                        Login
                    </a>
                </p>
            </div>
        </div>
    );
}