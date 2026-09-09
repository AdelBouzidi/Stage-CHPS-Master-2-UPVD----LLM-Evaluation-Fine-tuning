program find_closest
  implicit none
  integer :: n
  real, allocatable :: numbers(:)
  integer :: i, j, min_idx, min_idx2
  real :: min_diff, diff
  real :: result1, result2

  ! Read input
  read(*,*) n
  allocate(numbers(n))
  do i = 1, n
    read(*,*) numbers(i)
  end do

  ! Find the two closest elements
  min_diff = 1.0e30
  min_idx = 1
  min_idx2 = 2

  do i = 1, n
    do j = i + 1, n
      diff = abs(numbers(i) - numbers(j))
      if (diff < min_diff) then
        min_diff = diff
        min_idx = i
        min_idx2 = j
      end if
    end do
  end do

  ! Output the two closest elements in order
  if (numbers(min_idx) < numbers(min_idx2)) then
    result1 = numbers(min_idx)
    result2 = numbers(min_idx2)
  else
    result1 = numbers(min_idx2)
    result2 = numbers(min_idx)
  end if

  write(*,*) result1, result2

  deallocate(numbers)

end program find_closest