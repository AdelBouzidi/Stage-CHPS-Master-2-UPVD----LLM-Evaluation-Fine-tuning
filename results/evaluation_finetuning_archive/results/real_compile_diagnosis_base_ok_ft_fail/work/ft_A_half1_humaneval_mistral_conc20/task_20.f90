program find_closest_elements
  implicit none
  integer, parameter :: dp = kind(1.0d0)
  integer :: numbers_len
  real(dp), allocatable :: numbers(:)
  real(dp) :: closest1, closest2
  integer :: i, j, min_idx, min_j

  ! Read input
  read(*,*) numbers_len
  allocate(numbers(numbers_len))
  do i = 1, numbers_len
    read(*,*) numbers(i)
  end do

  ! Find the two closest numbers
  min_idx = 1
  min_j = 2
  do j = 2, numbers_len
    do i = 1, j-1
      if (abs(numbers(j) - numbers(i)) < abs(numbers(min_j) - numbers(min_idx))) then
        min_idx = i
        min_j = j
      end if
    end do
  end do

  closest1 = min(numbers(min_idx), numbers(min_j))
  closest2 = max(numbers(min_idx), numbers(min_j))

  ! Output result
  print *, closest1, closest2

end program find_closest_elements