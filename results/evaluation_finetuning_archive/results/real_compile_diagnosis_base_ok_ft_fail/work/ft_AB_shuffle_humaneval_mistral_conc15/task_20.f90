program find_closest_elements
  implicit none
  integer, parameter :: dp = kind(1.0d0)
  integer :: numbers_len
  real(dp), allocatable :: numbers(:)
  real(dp) :: closest1, closest2
  integer :: i, j, min_idx1, min_idx2
  real(dp) :: min_diff

  ! Hardcoded input data
  numbers_len = 6
  allocate(numbers(numbers_len))
  numbers = [1.0_dp, 2.0_dp, 3.0_dp, 4.0_dp, 5.0_dp, 2.2_dp]

  ! Find the two closest elements
  min_diff = huge(min_diff)
  min_idx1 = 1
  min_idx2 = 2

  do i = 1, numbers_len
    do j = i+1, numbers_len
      if (abs(numbers(i) - numbers(j)) < min_diff) then
        min_diff = abs(numbers(i) - numbers(j))
        min_idx1 = i
        min_idx2 = j
      end if
    end do
  end do

  closest1 = min(numbers(min_idx1), numbers(min_idx2))
  closest2 = max(numbers(min_idx1), numbers(min_idx2))

  print *, closest1, closest2

end program find_closest_elements