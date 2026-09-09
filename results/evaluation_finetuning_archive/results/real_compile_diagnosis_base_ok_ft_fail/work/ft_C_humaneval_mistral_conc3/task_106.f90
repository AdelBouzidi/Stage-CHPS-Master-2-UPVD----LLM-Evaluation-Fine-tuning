program factorial_sum
  implicit none
  integer :: n, i
  integer :: result
  integer, allocatable :: arr(:)

  ! Read input
  read(*,*) n

  ! Allocate array
  allocate(arr(n))

  ! Compute values
  do i = 1, n
    if (mod(i, 2) == 0) then
      ! Even index: factorial
      result = 1
      do j = 1, i
        result = result * j
      end do
      arr(i) = result
    else
      ! Odd index: sum from 1 to i
      result = 0
      do j = 1, i
        result = result + j
      end do
      arr(i) = result
    end if
  end do

  ! Print output
  do i = 1, n
    print *, arr(i)
  end do

  deallocate(arr)
end program factorial_sum