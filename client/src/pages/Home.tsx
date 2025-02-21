import FoobarForm from '@/components/Form/Foobar'

export default function Home() {
  return (
    <div className="flex h-screen w-full flex-col items-center justify-center gap-4">
      <h1 className="text-4xl font-medium">Doxic Spawn</h1>
      <FoobarForm />
    </div>
  )
}
