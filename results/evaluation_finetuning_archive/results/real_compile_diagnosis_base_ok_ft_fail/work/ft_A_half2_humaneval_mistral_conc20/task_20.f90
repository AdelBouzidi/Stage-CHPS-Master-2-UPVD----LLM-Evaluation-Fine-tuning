program find_closest_elements
  implicit none
  integer, parameter :: dp = kind(1.0d0)
  integer :: numbers_len
  real(dp), allocatable :: numbers(:)
  real(dp) :: closest1, closest2
  integer :: i, j, min_idx1, min_idx2
  real(dp) :: min_diff

  ! Read input
  read(*,*) numbers_len
  allocate(numbers(numbers_len))
  read(*,*) numbers

  ! Find the two closest numbers
  min_diff = huge(0.0_dp)
  min_idx1 = 1
  min_idx2 = 2

  do i = 1, numbers_len - 1
    do j = i + 1, numbers_len
      if (abs(numbers(i) - numbers(j)) < min_diff) then
        min_diff = abs(numbers(i) - numbers(j))
        min_idx1 = i
        min_idx2 = j
      end if
    end do
  end do

  ! Output the two closest numbers in order
  if (numbers(min_idx1) < numbers(min_idx2)) then
    print *, numbers(min_idx1), numbers(min_idx2)
  else
    print *, numbers(min_idx2), numbers(min_idx1)
  end if

end program find_closest_elements