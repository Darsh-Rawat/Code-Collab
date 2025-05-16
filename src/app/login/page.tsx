"use client"
import {
    Button,
    Field,
    Fieldset,
    For,
    Input,
    NativeSelect,
    Stack,
    AbsoluteCenter,
    Box,
} from "@chakra-ui/react"
import { PasswordInput } from "@/components/ui/password-input"



const page = () => {
    return (
        <Box minH="100vh"
            backgroundImage="url('/img.png')"
            backgroundSize="cover"
            backgroundPosition="center"
            backgroundRepeat="no-repeat">
            <AbsoluteCenter bg={"gray.900"} rounded={"2xl"} h={"60%"} w={"30%"}>
                <Fieldset.Root size="lg" maxW="md">
                    <Stack>
                        <Fieldset.Legend color={"blue.400"}>Contact details</Fieldset.Legend>
                        <Fieldset.HelperText color={"white"}>
                            Please provide your contact details below.
                        </Fieldset.HelperText>
                    </Stack>

                    <Fieldset.Content>
                        <Field.Root>
                            <Field.Label>Name</Field.Label>
                            <Input name="name" />
                        </Field.Root>

                        <Field.Root>
                            <Field.Label>Email address</Field.Label>
                            <Input name="email" type="email" />
                        </Field.Root>

                        <Field.Root>
                            <Field.Label>Password</Field.Label>
                            <PasswordInput />
                        </Field.Root>

                        <Field.Root>
                            <Field.Label>Country</Field.Label>
                            <NativeSelect.Root>
                                <NativeSelect.Field name="country">
                                    <For each={["United Kingdom", "Canada", "United States"]}>
                                        {(item) => (
                                            <option key={item} value={item}>
                                                {item}
                                            </option>
                                        )}
                                    </For>
                                </NativeSelect.Field>
                                <NativeSelect.Indicator />
                            </NativeSelect.Root>
                        </Field.Root>
                    </Fieldset.Content>

                    <Button type="submit" alignSelf="stretch" colorPalette={"blue"}>
                        Login
                    </Button>
                </Fieldset.Root>
            </AbsoluteCenter>
        </Box>

    )
}

export default page

