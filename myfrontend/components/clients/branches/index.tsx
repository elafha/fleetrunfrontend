import { Branch } from '@/interfaces'
import React from 'react'
import { AddBranch } from './add-branch'
import { SearchBranch } from './branch'
import dynamic from 'next/dynamic'
const BranchCard = dynamic(() => import('./branch'), { ssr: false })
import { faker } from '@faker-js/faker'
import { useClientsBranchesContext } from '@/context/clients/BranchesContext'

const Branches = () => {
  const { branches } = useClientsBranchesContext()

  return (
    <div className='w-full mx-auto flex flex-col items-center gap-y-6'>
      <SearchBranch />
      <div className='w-full flex flex-col items-center gap-y-6'>
        {branches.map((branch: Branch, index: number) => (
          <BranchCard key={index} branch={branch} />
        ))}
      </div>
      <AddBranch />
    </div>
  )
}

export default Branches
