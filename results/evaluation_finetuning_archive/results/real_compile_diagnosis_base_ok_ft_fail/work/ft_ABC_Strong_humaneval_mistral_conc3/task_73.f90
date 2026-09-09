program palindrome_change
  implicit none
  integer, parameter :: dp = selected_int_kind(18)
  integer(dp) :: arr_len
  integer(dp), allocatable :: arr(:)
  integer(dp) :: result

  ! Read input
  read(*,*) arr_len
  allocate(arr(arr_len))
  read(*,*) arr

  ! Calculate minimum changes needed
  result = 0
  do i = 1, arr_len/2
    if (arr(i) /= arr(arr_len - i + 1)) then
      result = result + 1
    end if
  end do

  ! Output result
  print(*,'(i0)') result

end program palindrome_change